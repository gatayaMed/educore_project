 #################Installation und Test-Anleitung###############
Option 1: Mit Docker (Empfohlen)
bash
# 1. In das Projektverzeichnis navigieren
cd educore_backend

# 2. Docker-Container starten
docker-compose up -d

# 3. Einen Superuser erstellen
docker-compose exec web python manage.py createsuperuser

# 4. Testdaten laden (optional)
docker-compose exec web python manage.py loaddata apps/kurse/fixtures/initial_courses.json

# 5. Server läuft unter http://localhost:8000
Option 2: Manuell (mit venv)
bash
# Linux/Mac
chmod +x setup.sh
./setup.sh

# Windows
setup.bat

# Server starten
python manage.py runserver
API Test mit curl
Nach dem Start können Sie die API testen:

bash
# 1. Token erhalten
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"ihr-passwort"}'

# 2. Kurse abrufen (mit Token)
curl -X GET http://localhost:8000/api/kurse/ \
  -H "Authorization: Token IHR_TOKEN_HIER"

# 3. Kursdetails abrufen
curl -X GET http://localhost:8000/api/kurse/1/ \
  -H "Authorization: Token IHR_TOKEN_HIER"

# 4. Anmeldung erstellen
curl -X POST http://localhost:8000/api/anmeldungen/ \
  -H "Authorization: Token IHR_TOKEN_HIER" \
  -H "Content-Type: application/json" \
  -d '{
    "kurs": 1,
    "vorname": "Max",
    "nachname": "Mustermann",
    "email": "max@example.com",
    "telefon": "0123-456789"
  }'
Wichtige Hinweise
PostgreSQL muss laufen - entweder über Docker oder lokal installiert

Token für API-Zugriff - jeder Request benötigt den Authorization-Header

Tests ausführen: python manage.py test

Swagger-Dokumentation: http://localhost:8000/swagger/

Admin-Interface: http://localhost:8000/admin/

Dieser Code enthält alle 3 API-Endpunkte (GET /kurse/, GET /kurse/{id}/, POST /anmeldungen/) mit vollständiger Business-Logik (Kapazitätsprüfung, Doppelanmeldungsschutz) und Token-Authentifizierung.

