#!/bin/bash

echo "=== educore Backend Setup ==="

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Load initial data
echo "Loading initial course data..."
python manage.py loaddata apps/kurse/fixtures/initial_courses.json

echo ""
echo "=== Setup Complete ==="
echo "Run: python manage.py runserver"
echo "Admin: http://localhost:8000/admin/"
echo "API: http://localhost:8000/api/kurse/"
echo "Swagger: http://localhost:8000/swagger/"