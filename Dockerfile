# Use Python 3.11+ for Django 5.x compatibility
FROM python:3.11-alpine

# Maintainer info (Optional)
LABEL maintainer="localhost:8000"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add --no-cache postgresql-client libjpeg-turbo

# Install build dependencies (temporarily)
RUN apk add --no-cache --virtual .build-deps \
    gcc python3-dev postgresql-dev musl-dev zlib-dev jpeg-dev

# Set working directory
WORKDIR /DjangoKickstart

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Remove build dependencies to reduce image size
RUN apk del --no-cache .build-deps

# Copy application files
COPY . .

# Create a user (optional for security)
RUN addgroup -g 994 jenkins && adduser -D -u 997 jenkins -G jenkins

# Set user permissions (optional)
USER jenkins

# Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]