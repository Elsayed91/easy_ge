FROM python:3.10.7-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add the poetry installation and configuration
RUN pip install --no-cache-dir poetry==1.5.1

# Copy the rest of the working directory contents into the container at /app
COPY . /app/

# Install the project dependencies and make the entrypoint.py script executable
RUN poetry install -E google --no-dev --no-root \
    && chmod +x /app/entrypoint.py

# Set the working directory for the container when it starts
WORKDIR /data

# Run the command inside the virtual environment created by poetry
ENTRYPOINT ["poetry", "run", "python", "/app/entrypoint.py"]

# Set the default command to run when the container starts
CMD ["--config", "/data/config.yaml"]
