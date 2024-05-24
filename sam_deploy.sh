#!/bin/bash

# Source the environment variables
set -a # automatically export all variables
source .env
set +a # stop automatically exporting variables

if [ "$1" == "app" ]; then
    TEMPLATE_FILE="app_template.yaml"
    CONFIG_ENV="AppStack"
    STACK_NAME="url-shortener-app-stack-$2"
elif [ "$1" == "certificate" ]; then
    TEMPLATE_FILE="certificate_template.yaml"
    CONFIG_ENV="CertificateStack"
    STACK_NAME="url-shortener-certificate-stack-$2"
else
    echo "Invalid parameter. Please use either 'app' or 'certificate'."
    exit 1
fi

# Run sam deploy with the environment variables
sam deploy --template-file $TEMPLATE_FILE --config-env $CONFIG_ENV --stack-name $STACK_NAME --s3-prefix $STACK_NAME --parameter-overrides PersonalAcessToken=$GITHUB_TOKEN CloudflareApiToken=$CLOUDFLARE_TOKEN AppName=$STACK_NAME GithubRepository=$GITHUB_REPO