#!/bin/bash
set -e
DEFAULT_REGION="us-east-1"
STACK_NAME="unionize"
S3_BUCKET="unionize-bucket"

echo -e "\n>>> Building stack $STACK_NAME\n"
sam build -t infrastructure/cloud-formation/template.yml -s ./src \
    --region ${DEFAULT_REGION} \
    --use-container

echo -e "\n>>> Deploying stack $STACK_NAME\n"
sam deploy --stack-name $STACK_NAME \
    --s3-bucket $S3_BUCKET \
    --s3-prefix $STAC_KNAME \
    --region $DEFAULT_REGION \
    --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND \
    --confirm-changeset

echo -e "\n>>> Deployment complete for $STACK_NAME\n"