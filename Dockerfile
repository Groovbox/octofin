# Use an official Python image as the base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set work directory
WORKDIR /app

# Copy only the dependency files first for caching
COPY pyproject.toml poetry.lock ./

# Install dependencies (no virtualenv, install to system)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project code
COPY . .

# Expose the port Django runs on
EXPOSE 3936

# Run Django migrations and start the server
CMD ["python", "src/manage.py", "migrate"]
# For development, you might want:
# CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
