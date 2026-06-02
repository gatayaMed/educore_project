# backend/Dockerfile
FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8100 (matches your compose file)
EXPOSE 8100

# Run gunicorn (no nginx needed for Coolify)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8100", "--workers", "3", "--timeout", "120"]