"""
Django settings for CyberHealth project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ
import os
from pathlib import Path
import logging
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ABS_ROOT = os.path.abspath(os.path.dirname(__name__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

# This application requires a secret key to be set in the environment to be run
SECRET_KEY = env('SECRET_KEY')

# This application requires a debug flag to be set

DEBUG = env('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.london.cloudapps.digital']

# Application definition

INSTALLED_APPS = [
    'staticpages.apps.StaticpagesConfig',
    'assessment.apps.AssessmentConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'basicauth.middleware.BasicAuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CyberHealth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CyberHealth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# https://django-environ.readthedocs.io/en/latest/
# This relies on DATABASE_URL being available in the environment

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = os.path.join(BASE_DIR, 'static/')
STATIC_ROOT = os.path.join(STATIC_URL, 'assets')
STATICFILES_DIRS = [
    os.path.join(STATIC_URL, 'dist'), 
]

BASICAUTH_USERS = {'CyberHealth': 'cyber123'}
BASICAUTH_DISABLE = env('BASICAUTH_DISABLE', default=True)

# Adding in logging
# If you're following the Twelve-Factor App methodology for your application,
# then you'll want to send your logs to Stdout.
# https://odwyer.software/blog/logging-to-standard-output-with-django

LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
       'verbose': {
           'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
       },
   },
   'handlers': {
       'console': {
           'level': 'INFO',
           'class': 'logging.StreamHandler',
           'stream': sys.stdout,
           'formatter': 'verbose'
       },
   },
   'loggers': {
       '': {
           'handlers': ['console'],
           'level': 'INFO',
           'propagate': True,
       },
   },
}
