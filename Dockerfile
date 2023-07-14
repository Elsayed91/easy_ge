FROM python:3.10.7-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY . /app/

# Add the poetry installation and dependencies
RUN pip install --no-cache-dir poetry==1.5.1 \
    && poetry install -E google --no-dev --no-root

COPY --chmod=755 entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["--config", "/app/config.yaml"]