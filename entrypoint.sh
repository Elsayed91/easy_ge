#!/bin/sh
if [ -n "$GCS_CREDENTIALS_FILE" ]; then
    export GOOGLE_APPLICATION_CREDENTIALS="/app/$GCS_CREDENTIALS_FILE"
fi

if [ -n "$S3_ACCESS_KEY" ] && [ -n "$S3_SECRET_KEY" ]; then
    export AWS_ACCESS_KEY_ID="$S3_ACCESS_KEY"
    export AWS_SECRET_ACCESS_KEY="$S3_SECRET_KEY"
fi

# Run the command inside the virtual environment created by poetry
poetry run python -m /app/easy_ge/entrypoint.py "$@"
