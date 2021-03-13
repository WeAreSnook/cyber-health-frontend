#!/bin/bash

node accessibility/index.js

APPLICATIONS=("frontend")

for application in "${APPLICATIONS[@]}"
do
    (
        echo "runnning dependency check on ./$application"
        dependency-check/bin/dependency-check.sh --project "$application" --scan "./$application"
    )
done