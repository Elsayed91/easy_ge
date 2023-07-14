FROM python:3.10.7-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY . /app/

# Add the poetry installation and configuration
RUN pip install --no-cache-dir poetry==1.5.1


# Install the project dependencies
RUN poetry install -E google --no-dev --no-root

# Copy the rest of the working directory contents into the container at /app



# Modify the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["--config", "/app/config.yaml"]