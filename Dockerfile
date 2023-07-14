FROM python:3.10.7-slim-bullseye
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock* .
RUN pip install --no-cache-dir poetry==1.5.1 && poetry install --no-dev --no-root
COPY . .
ENTRYPOINT ["python", "-m", "easy_ge.main"]

# Use an official Python runtime as a parent image
FROM python:3.10.7-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add the poetry installation and configuration
RUN pip install --no-cache-dir poetry==1.5.1

# Copy the rest of the working directory contents into the container at /app
COPY . /app/

# Install the project dependencies.
# This is done by first copying the pyproject.toml file and running poetry install.
# If a lock file exists, it will be used, otherwise poetry will create one.
COPY pyproject.toml poetry.lock* /app/
RUN poetry install -E google --no-dev --no-root


# Make sure the entrypoint.py script is executable
RUN chmod +x /app/entrypoint.py

# Run the command inside the virtual environment created by poetry
ENTRYPOINT ["poetry", "run", "python", "/app/entrypoint.py"]

# Set the working directory for the container when it starts
WORKDIR /data

# Set the default command to run when the container starts
CMD ["--config", "/data/config.yaml"]
