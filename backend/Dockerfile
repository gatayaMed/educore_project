# backend/Dockerfile
FROM python:3.11-slim-bookworm

# Set Python environment variables (critical for production)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Collect static files (no DB connection needed)
RUN python manage.py collectstatic --noinput

EXPOSE 8100

# Run migrations and start gunicorn (like working example)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8100 --workers 3 --timeout 120 --log-level info"]