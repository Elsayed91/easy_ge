FROM python:3.10.7-slim-bullseye
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock* .
RUN pip install --no-cache-dir poetry==1.5.1 && poetry install --no-dev --no-root
COPY . .
ENTRYPOINT ["python", "-m", "easy_ge.main"]
