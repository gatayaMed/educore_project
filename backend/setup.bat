@echo off
echo === educore Backend Setup ===

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser

REM Load initial data
echo Loading initial course data...
python manage.py loaddata apps/kurse/fixtures/initial_courses.json

echo.
echo === Setup Complete ===
echo Run: python manage.py runserver
echo Admin: http://localhost:8000/admin/
echo API: http://localhost:8000/api/kurse/
echo Swagger: http://localhost:8000/swagger/
pause