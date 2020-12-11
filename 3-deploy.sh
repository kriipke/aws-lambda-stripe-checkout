#!/bin/bash
set -eo pipefail
ARTIFACT_BUCKET="xtal-devops"
aws cloudformation package --template-file template.yml --s3-bucket $ARTIFACT_BUCKET --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name stripe-checkout --capabilities CAPABILITY_NAMED_IAM
