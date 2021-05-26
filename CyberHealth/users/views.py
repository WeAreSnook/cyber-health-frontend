from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from .models import Organisation, OrganisationUser, UserProfile
from django.contrib import messages
from django.conf import settings
import uuid


def send_user_notification(user_details, user_token,
                           template_id='63d94931-3b5a-42dc-ba0d-06b40902298b'):
    return settings.NOTIFICATIONS_CLIENT.send_email_notification(
        email_address=user_details.email,
        template_id=template_id,
        personalisation={
            'first_name': user_details.first_name,
            'account_verification': f'http://127.0.0.1:8000/account_verification/{user_token}',
        }
    )


def get_message_status(notification_id):
    message_status = ''
    while message_status.lower() != 'delivered':
        message_status = settings.NOTIFICATIONS_CLIENT.get_notification_by_id(notification_id).get('status')
    return message_status


def deactivate_user(user_details):
    deactivated_user = User.objects.get(username=user_details.username)
    deactivated_user.is_active = False
    deactivated_user.save()


def activate_user(user_details):
    activated_user = User.objects.get(username=user_details.username)
    activated_user.is_active = True
    activated_user.save()


def account_activation(request, auth_token):
    try:
        user_profile_details = UserProfile.objects.filter(auth_token=auth_token).first()
        if user_profile_details:
            if user_profile_details.is_verified:
                messages.success(request, 'This account is already verified.')
                return redirect('login')
            activate_user(user_profile_details.user)
            user_profile_details.is_verified = True
            user_profile_details.save()
            return redirect('success-page')
        else:
            messages.error(request, 'The requested profile does not exist.')
            return redirect('register')
    except Exception as e:
        print(e)
        return render(request, error_page(request))


def error_page(request):
    return render(request, 'users/error_page.html')


def success_page(request):
    return render(request, 'users/success.html')


def send_token_page(request):
    return render(request, 'users/send_token.html')


def user_registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                print(form.cleaned_data.get('email'))
                organisation = Organisation.objects.get(
                    domain_name=form.cleaned_data.get('email').split('@')[-1])
                organisation_user = OrganisationUser.objects.filter(
                    user_organisation=organisation).first()
                if organisation_user is None and organisation:
                    user_info = form.save(commit=False)
                    auth_token = str(uuid.uuid4())
                    send_user_notification(user_info, auth_token)
                    user_info.username = user_info.email
                    user_info.save()
                    deactivate_user(user_info)
                    organisation.organisation_users_info.add(user_info)
                    user_profile = UserProfile.objects.create(
                        user=user_info, auth_token=auth_token)
                    user_profile.save()
                    return redirect('send-token-page')
                else:
                    messages.info(request, 'There is already a user for '
                                  'your local council.')
            except Exception as e:
                print(e)
                messages.error(request, 'There was an error in the sign up'
                                        ' process. Please check the details '
                                        'provided e.g. the email address.'
                                        'Please try again.')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

