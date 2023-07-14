#!/bin/bash
set -e

# docker pull localstack/localstack
SERVICES=s3 localstack start -d
localstack wait -t 30 
echo "Startup complete"

awslocal s3 mb s3://mybucket
awslocal s3 cp tests/test_configs/expectations/yellow.json s3://mybucket/expectations/

python -c "from easy_ge import easy_validation; easy_validation('tests/test_configs/sample_config.yaml')"

echo "run_validation exited without error, checking if artifacts were loaded to S3"
awslocal s3 ls s3://mybucket/expectations/ | grep -q yellow.json || (echo 'Expectations directory is empty' && exit 1)
awslocal s3 ls s3://mybucket/validations/ | grep -q .ge_store_backend_id || (echo 'Validations directory is empty' && exit 1)
awslocal s3 ls s3://mybucket/docs/ | grep -q 'index.html' || (echo 'Docs directory is empty' && exit 1)

echo "looking to see if CSV was downloaded."
FILENAME=yellow-$(date +%Y-%m-%d).csv
test -f $FILENAME && echo "File $FILENAME exists." || exit 1
echo "Test Execution complete!" 
rm $FILENAME

localstack stop