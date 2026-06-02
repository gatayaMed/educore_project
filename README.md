📚 Educore - E-Learning Kursverwaltungsplattform
<div align="center">
https://img.shields.io/badge/Python-3.11-blue.svg
https://img.shields.io/badge/Django-4.2-green.svg
https://img.shields.io/badge/DRF-3.14-red.svg
https://img.shields.io/badge/PostgreSQL-15-blue.svg
https://img.shields.io/badge/Docker-Ready-2496ED.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/WebSocket-Realtime-ff69b4.svg

Eine moderne E-Learning-Plattform für Kursverwaltung und Online-Anmeldungen

Features • Quick Start • Installation • API Dokumentation • Deployment

</div>
🎯 Über Educore
Educore ist eine umfassende E-Learning-Plattform, die Bildungsanbietern und Kursteilnehmern eine nahtlose Verwaltung von Kursen und Anmeldungen ermöglicht. Die Plattform bietet eine intuitive REST-API für die Integration in verschiedene Frontends und Systeme.

🌟 Kernkonzept
Educore wurde entwickelt, um Bildungsinstitutionen bei der digitalen Transformation zu unterstützen. Statt komplexer manueller Prozesse bietet Educore eine automatisierte Kursverwaltung mit Echtzeit-Kapazitätsprüfungen, Doppelanmeldungsschutz und einer benutzerfreundlichen API-Schnittstelle.

🎯 Warum "Educore"?
Edu (Education) - Fokus auf Bildungsmanagement

Core (Kern) - Zentrale Plattform für alle Kursaktivitäten

Core (dt. Kern) - Das Herzstück Ihrer Bildungsverwaltung

Einsatzbereiche:

Universitäten und Hochschulen 🎓

Berufliche Weiterbildungszentren 💼

Sprachschulen 🌍

Musikschulen 🎵

Fitnessstudios und Yogaschulen 🧘

Online-Kursplattformen 💻

✨ Hauptfunktionen
Für Administratoren & Kursanbieter
✅ Vollständige Kursverwaltung - Erstellen, bearbeiten und löschen von Kursen

✅ Kapazitätsmanagement - Automatische Auslastungsberechnung

✅ Teilnehmerverwaltung - Zentrale Verwaltung aller Kursteilnehmer

✅ Anmeldungsübersicht - Echtzeit-Einblick in alle Anmeldungen

✅ Admin Dashboard - Intuitive Verwaltungsoberfläche

✅ Datenexport - Export von Kurs- und Teilnehmerdaten

Für Kursteilnehmer
✅ Kurskatalog - Durchsuchen aller verfügbaren Kurse

✅ Detailinformationen - Umfassende Kursbeschreibungen und Termine

✅ Online-Anmeldung - Einfache Selbstanmeldung für Kurse

✅ Kapazitätsanzeige - Echtzeit-Verfügbarkeit der Kursplätze

✅ Personalisierte Übersicht - Eigene Anmeldungen einsehen

API & Technische Features
🔒 Token-basierte Authentifizierung - Sichere API-Zugriffe

📝 Automatische API-Dokumentation - Swagger/OpenAPI Support

🔍 Erweiterte Suchfunktionen - Filtern nach Datum, Verfügbarkeit

📊 Paginierung - Effizientes Laden großer Datenmengen

🐳 Docker Ready - Containerisierte Bereitstellung

🚀 High Performance - Optimierte Datenbankabfragen

🏗️ Architektur
text
┌─────────────────────────────────────────────────────────────┐
│                       Educore Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐ │
│  │   React     │      │   Mobile    │      │  Third-     │ │
│  │  Frontend   │      │     App     │      │  Party API  │ │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘ │
│         │                    │                    │         │
│         └────────────────────┼────────────────────┘         │
│                              │                              │
│                              ▼                              │
│         ┌──────────────────────────────────────┐           │
│         │         REST API (Django DRF)        │           │
│         │    - Token Authentication            │           │
│         │    - Serializers                     │           │
│         │    - ViewSets & APIViews             │           │
│         └────────────┬────────────┬────────────┘           │
│                      │            │                          │
│          ┌───────────▼────┐   ┌───▼────────────┐            │
│          │   PostgreSQL   │   │   Business     │            │
│          │   Database     │   │    Logic       │            │
│          └────────────────┘   └────────────────┘            │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Datenbankmodell:
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    Kurse     │     │  Teilnehmer  │     │  Anmeldungen │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ id (PK)      │     │ id (PK)      │     │ id (PK)      │
│ titel        │     │ vorname      │     │ kurs (FK)    │
│ beschreibung │     │ nachname     │     │ teilnehmer   │
│ start_datum  │     │ email (uniq) │     │ anmeldedatum │
│ end_datum    │◄────┤ telefon      │────►│ status       │
│ max_teilnehmer│     └──────────────┘     └──────────────┘
└──────────────┘
📋 Inhaltsverzeichnis
Über Educore

Hauptfunktionen

Architektur

Quick Start

Installation

Docker Setup

API Dokumentation

Frontend Integration

Coolify Deployment

Testing

Troubleshooting

FAQ

Mitwirken

Lizenz

🚀 Quick Start
Voraussetzungen
Python 3.11 oder höher

PostgreSQL 15+ (oder SQLite für Entwicklung)

Docker & Docker Compose (für Container-Deployment)

Git

Ein-Klick-Setup mit Docker
bash
# 1. Repository klonen
git clone https://github.com/yourusername/educore-backend.git
cd educore-backend

# 2. Mit Docker Compose starten
docker-compose up -d

# 3. Datenbankmigrationen ausführen
docker-compose exec web python manage.py migrate

# 4. Superuser erstellen
docker-compose exec web python manage.py createsuperuser

# 5. Server läuft unter http://localhost:8000
Manuelle Installation (mit venv)
bash
# 1. Repository klonen
git clone https://github.com/yourusername/educore-backend.git
cd educore-backend

# 2. Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeiten Sie .env mit Ihren Werten

# 5. Datenbank einrichten
python manage.py migrate

# 6. Superuser erstellen
python manage.py createsuperuser

# 7. Static files sammeln
python manage.py collectstatic

# 8. Server starten
python manage.py runserver
📦 Installation
Detaillierte Installationsanleitung
1. System-Abhängigkeiten (Ubuntu/Debian)
bash
# System aktualisieren
sudo apt update && sudo apt upgrade -y

# Python und Entwicklungstools installieren
sudo apt install -y python3.11 python3-pip python3-dev
sudo apt install -y postgresql postgresql-contrib libpq-dev
sudo apt install -y redis-server  # Optional für Caching/WebSockets
2. PostgreSQL Datenbank einrichten
bash
# PostgreSQL Dienst starten
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Datenbank und Benutzer erstellen
sudo -u postgres psql

-- In der PostgreSQL Shell:
CREATE DATABASE educore;
CREATE USER educore_user WITH PASSWORD 'educore_password';
ALTER ROLE educore_user SET client_encoding TO 'utf8';
ALTER ROLE educore_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE educore_user SET timezone TO 'Europe/Berlin';
GRANT ALL PRIVILEGES ON DATABASE educore TO educore_user;
\q
3. Projekt konfigurieren
bash
# Umgebungsvariablen setzen
export SECRET_KEY='your-super-secret-key-here'
export DEBUG=False
export DB_NAME=educore
export DB_USER=educore_user
export DB_PASSWORD=educore_password
export DB_HOST=localhost
export DB_PORT=5432
4. Testdaten laden (optional)
bash
# Beispielkurse importieren
python manage.py loaddata apps/kurse/fixtures/initial_courses.json
🐳 Docker Setup
Dockerfile (Produktion)
dockerfile
FROM python:3.11-slim-bookworm

# System-Abhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projekt kopieren
COPY . .

# Static files sammeln
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
docker-compose.yml
yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: educore
      POSTGRES_USER: educore_user
      POSTGRES_PASSWORD: educore_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_NAME=educore
      - DB_USER=educore_user
      - DB_PASSWORD=educore_password

volumes:
  postgres_data:
Docker Befehle
bash
# Container im Hintergrund starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f web

# Migrationen ausführen
docker-compose exec web python manage.py migrate

# Shell im Container öffnen
docker-compose exec web bash

# Container stoppen
docker-compose down

# Mit Datenbankverbindung
docker-compose exec db psql -U educore_user -d educore
📖 API Dokumentation
Authentifizierung
Alle API-Endpunkte (außer Token-Erstellung) benötigen ein Authentifizierungstoken:

bash
# 1. Token erhalten
POST /api-token-auth/
Content-Type: application/json

{
    "username": "admin",
    "password": "your-password"
}

# Response
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}

# 2. Token in API-Requests verwenden
GET /api/kurse/
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
API Endpunkte
Kurse verwalten
Methode	Endpoint	Beschreibung
GET	/api/kurse/	Alle Kurse auflisten (paginiert)
GET	/api/kurse/{id}/	Kursdetails anzeigen
GET	/api/kurse/?search=Python	Kurse suchen
GET	/api/kurse/?only_future=true	Nur zukünftige Kurse
Response Beispiel:

json
{
    "count": 10,
    "next": "http://localhost:8000/api/kurse/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "titel": "Python Grundkurs",
            "beschreibung": "Lernen Sie die Grundlagen von Python",
            "start_datum": "2024-03-01",
            "end_datum": "2024-04-30",
            "max_teilnehmer": 20,
            "verfuegbare_plaetze": 15,
            "ist_voll": false,
            "erstellt_am": "2024-01-15T10:00:00Z",
            "aktualisiert_am": "2024-01-15T10:00:00Z"
        }
    ]
}
Anmeldungen
Methode	Endpoint	Beschreibung
POST	/api/anmeldungen/	Neue Anmeldung erstellen
Request Body:

json
{
    "kurs": 1,
    "vorname": "Max",
    "nachname": "Mustermann",
    "email": "max@example.com",
    "telefon": "+49123456789"
}
Response (201 Created):

json
{
    "id": 42,
    "kurs": 1,
    "kurs_titel": "Python Grundkurs",
    "teilnehmer": 5,
    "teilnehmer_name": "Max Mustermann",
    "anmeldedatum": "2024-01-20T14:30:00Z",
    "status": "angemeldet"
}
Fehlercodes
Code	Bedeutung	Lösung
200	Erfolg	-
201	Erstellt	-
400	Ungültige Anfrage	Request validieren
401	Nicht authentifiziert	Token prüfen
403	Keine Berechtigung	Rechte prüfen
404	Nicht gefunden	ID überprüfen
409	Konflikt	Doppelte Anmeldung
Swagger/OpenAPI Dokumentation
Nach dem Start verfügbar unter:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

OpenAPI Schema: http://localhost:8000/api/schema/

🎨 Frontend Integration
Beispiele für verschiedene Frontends
React mit Fetch API
javascript
// Authentifizierung
const login = async (username, password) => {
    const response = await fetch('http://localhost:8000/api-token-auth/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    localStorage.setItem('token', data.token);
    return data;
};

// Kurse laden
const fetchCourses = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/kurse/', {
        headers: { 'Authorization': `Token ${token}` }
    });
    return await response.json();
};

// Anmeldung erstellen
const enrollInCourse = async (courseId, userData) => {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/api/anmeldungen/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
            kurs: courseId,
            ...userData
        })
    });
    return await response.json();
};
Vue.js mit Axios
javascript
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/'
});

// Interceptor für Token
api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

// API Calls
export const courseService = {
    getAll: () => api.get('/kurse/'),
    getById: (id) => api.get(`/kurse/${id}/`),
    enroll: (data) => api.post('/anmeldungen/', data)
};
HTML/JavaScript (Vanilla)
html
<!-- Siehe die im Frontend-Teil erstellten HTML Dateien -->
<script>
    // Im Frontend-Teil bereits implementiert
    // Verwendung von Bootstrap 5 für das UI
</script>
🚀 Coolify Deployment
Schritt-für-Schritt Deployment auf Coolify
Phase 1: Repository vorbereiten
bash
# 1. SSH Key für Coolify generieren (lokal)
ssh-keygen -t ed25519 -C "coolify-deploy" -f ~/.ssh/coolify-deploy

# 2. Öffentlichen Key zu GitHub Deploy Keys hinzufügen
cat ~/.ssh/coolify-deploy.pub
# Kopieren und in GitHub → Settings → Deploy keys einfügen

# 3. Repository pushen
git add .
git commit -m "Add production configuration"
git push origin main
Phase 2: VPS konfigurieren
bash
# 1. Auf VPS einloggen
ssh root@your-vps-ip

# 2. Firewall konfigurieren
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 3. Coolify installieren
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash

# 4. Coolify Dashboard aufrufen
# Öffnen Sie http://your-vps-ip:3000 in Ihrem Browser
Phase 3: Coolify einrichten
Admin Account erstellen

Server hinzufügen (localhost)

Traefik Proxy starten

Settings → Proxy → Start Traefik

Let's Encrypt Email eintragen

GitHub Repository verbinden

Project → New Resource → Git Repository

Build Pack: Docker Compose

Phase 4: Umgebungsvariablen setzen
In Coolify UI folgende Variablen setzen:

env
SECRET_KEY=your-super-secret-key
DEBUG=False
ALLOWED_HOSTS=educore.yourdomain.com
DB_HOST=postgres
DB_NAME=educore
DB_USER=educore_user
DB_PASSWORD=StrongPassword123!
CORS_ALLOWED_ORIGINS=https://educore.yourdomain.com
Phase 5: Persistent Storage konfigurieren
Service	Host Path	Container Path
django	/data/coolify/volumes/educore_media	/app/media
django	/data/coolify/volumes/educore_static	/app/staticfiles
Phase 6: Deploy
bash
# In Coolify UI auf "Deploy" klicken

# Nach erfolgreichem Deployment:
# 1. Migrationen ausführen
docker exec $(docker ps -q -f name=educore-django) python manage.py migrate

# 2. Superuser erstellen
docker exec -it $(docker ps -q -f name=educore-django) python manage.py createsuperuser

# 3. SSL-Zertifikat prüfen
# Warten Sie 2-3 Minuten, dann ist HTTPS automatisch aktiv
Domain konfigurieren
bash
# DNS-Einträge (bei Ihrem Domain-Provider)
Type    Name                    Value
A       educore                 your-vps-ip
CNAME   www.educore             educore.yourdomain.com
🧪 Testing
Test-Abhängigkeiten installieren
bash
pip install pytest pytest-django pytest-cov factory-boy
Tests ausführen
bash
# Alle Tests
python manage.py test

# Bestimmte App testen
python manage.py test apps.kurse

# Mit Coverage
coverage run manage.py test
coverage report
coverage html  # HTML Report in htmlcov/
Test-Beispiele
python
# apps/anmeldungen/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from apps.kurse.models import Kurs

class EnrollmentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.force_authenticate(user=self.user)
        
        self.course = Kurs.objects.create(
            titel="Test Kurs",
            beschreibung="Test Beschreibung",
            start_datum="2024-03-01",
            end_datum="2024-04-30",
            max_teilnehmer=10
        )
    
    def test_create_enrollment_success(self):
        data = {
            "kurs": self.course.id,
            "vorname": "Max",
            "nachname": "Mustermann",
            "email": "max@example.com"
        }
        response = self.client.post('/api/anmeldungen/', data)
        self.assertEqual(response.status_code, 201)
    
    def test_course_full_validation(self):
        # Fülle alle Plätze
        for i in range(self.course.max_teilnehmer):
            self.course.anmeldungen.create(
                teilnehmer_id=i+1,
                status='angemeldet'
            )
        
        data = {
            "kurs": self.course.id,
            "vorname": "Extra",
            "nachname": "Teilnehmer",
            "email": "extra@example.com"
        }
        response = self.client.post('/api/anmeldungen/', data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("ausgebucht", str(response.data))
🔧 Troubleshooting
Häufige Probleme und Lösungen
Problem 1: Datenbankverbindung fehlgeschlagen
bash
# Symptom: "could not connect to server: Connection refused"

# Lösung:
# 1. PostgreSQL Status prüfen
sudo systemctl status postgresql

# 2. In Docker: Netzwerk prüfen
docker-compose logs db

# 3. Hostname in settings.py prüfen
# Bei Docker: DB_HOST=db (Service-Name)
# Bei lokal: DB_HOST=localhost
Problem 2: Static files werden nicht geladen
bash
# Symptom: 404 auf /static/ Dateien

# Lösung:
python manage.py collectstatic --noinput
python manage.py findstatic --verbosity 2 styles.css

# In Docker:
docker-compose exec web python manage.py collectstatic --noinput
Problem 3: Token-Authentifizierung funktioniert nicht
bash
# Symptom: "Invalid token" oder 401

# Lösung:
# 1. Token im Header korrekt formatieren
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# 2. Token in der Datenbank prüfen
python manage.py shell
>>> from rest_framework.authtoken.models import Token
>>> Token.objects.all().values('user__username', 'key')

# 3. Neuen Token generieren
python manage.py drf_create_token admin
Problem 4: CORS Fehler im Frontend
javascript
// Symptom: "Access-Control-Allow-Origin" Fehler

// Lösung in settings.py:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True
Problem 5: SSL Probleme bei Coolify
bash
# Symptom: Falsches SSL-Zertifikat

# Lösung:
# 1. DNS prüfen
dig educore.yourdomain.com

# 2. Traefik Cache leeren
docker stop coolify-proxy
rm /data/coolify/proxy/acme.json
docker start coolify-proxy

# 3. Let's Encrypt Email in Coolify Settings prüfen
❓ FAQ
Allgemeine Fragen
F: Kann ich SQLite statt PostgreSQL verwenden?
A: Ja, für Entwicklung. Kommentieren Sie einfach die PostgreSQL-Konfiguration in settings.py aus.

F: Wie passe ich das Frontend an?
A: Das Frontend ist komplett in HTML/CSS/JS mit Bootstrap 5. Alle Dateien sind im Frontend-Teil dokumentiert.

F: Unterstützt Educore mehrere Sprachen?
A: Ja, die Plattform ist auf Deutsch und Englisch vorbereitet (USE_I18N = True).

F: Wie skaliere ich die Anwendung?
A: Verwenden Sie Gunicorn mit mehreren Workern und setzen Sie einen Load Balancer (z.B. Nginx) davor.

Technische Fragen
F: Welche Python-Version wird benötigt?
A: Python 3.11 oder höher.

F: Benötige ich Redis?
A: Nur für WebSocket/Channels. Für die Basis-API ist Redis optional.

F: Wie sichere ich die API?
A: Verwenden Sie Token-Authentifizierung, HTTPS, und setzen Sie DEBUG=False in Produktion.

F: Kann ich die API mit Postman testen?
A: Ja! Importieren Sie die OpenAPI-Spezifikation von /api/schema/.

🤝 Mitwirken
Beiträge sind willkommen! So können Sie helfen:

Fork das Repository

Feature Branch erstellen (git checkout -b feature/AmazingFeature)

Commit Ihre Änderungen (git commit -m 'Add some AmazingFeature')

Push zum Branch (git push origin feature/AmazingFeature)

Pull Request öffnen

Entwicklungsumgebung einrichten
bash
# 1. Fork clonen
git clone https://github.com/YOUR_USERNAME/educore-backend.git
cd educore-backend

# 2. Virtuelle Umgebung
python -m venv venv
source venv/bin/activate

# 3. Entwicklungsabhängigkeiten
pip install -r requirements.txt
pip install pytest pytest-django black flake8 pre-commit

# 4. Pre-commit Hooks einrichten
pre-commit install

# 5. Tests ausführen
pytest
📄 Lizenz
Dieses Projekt ist unter der MIT Lizenz lizenziert - siehe die LICENSE Datei für Details.

🙏 Danksagungen
Django Community - Für das großartige Framework

Django REST Framework - Für die API-Funktionalität

Bootstrap Team - Für das responsive Design

PostgreSQL - Für die zuverlässige Datenbank

Coolify Team - Für das einfache Deployment

📞 Kontakt & Support
Dokumentation: https://docs.educore.com

Issue Tracker: GitHub Issues

Discord Community: https://discord.gg/educore

Email Support: support@educore.com

<div align="center">
Made with ❤️ by the Educore Team

⬆ Back to Top

</div>