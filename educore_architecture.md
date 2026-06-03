Educore Architecture
High-Level Overview
User Browser
     │
     ▼
Traefik (Reverse Proxy)
     │
     ├──► Frontend (nginx) ──► Static HTML/CSS/JS
     │         educore.smarta.website/*
     │
     └──► Backend (Django) ──► PostgreSQL
               educore.smarta.website/api/*
               educore.smarta.website/admin/*
               educore.smarta.website/api-token-auth/*

Layer by Layer
Layer 1 — Frontend (nginx)
Static files only — no server-side logic. Three pages:

index.html — landing page, loads featured courses
courses.html — course listing with search and filter
course-detail.html — course details + enrollment modal

JavaScript handles everything dynamically:
utils.js     → helper functions (formatDate, escapeHtml, debounce)
api.js       → all HTTP calls to backend (apiRequest function)
auth.js      → token storage, login/logout, navbar state
courses.js   → load and display courses
enrollment.js → enrollment form submission
Layer 2 — Backend (Django REST Framework)
Three apps, three responsibilities:
apps/
├── kurse/          → Course management (read-only API)
├── teilnehmer/     → Participant management (full CRUD)
└── anmeldungen/    → Enrollment logic (create only)
Only 3 API endpoints exposed:
GET  /api/kurse/          → list all courses (paginated)
GET  /api/kurse/{id}/     → course details + enrollment count
POST /api/anmeldungen/    → create enrollment
POST /api-token-auth/     → get auth token (login)
Layer 3 — Database (PostgreSQL)
Three tables mirroring the Django apps:
kurse        → id, titel, beschreibung, start_datum, end_datum, max_teilnehmer
teilnehmer   → id, vorname, nachname, email, telefon
anmeldungen  → id, kurs_id, teilnehmer_id, status, anmeldedatum
              (unique_together: kurs + teilnehmer)

Authentication Flow
1. User submits login form
2. Frontend POST /api-token-auth/ {username, password}
3. Django returns {"token": "abc123..."}
4. Frontend stores token in localStorage
5. Every subsequent API request sends:
   Authorization: Token abc123...
6. Django validates token on each request

Enrollment Flow (most complex business logic)
1. User clicks "Anmelden" on course detail page
2. Modal form collects: vorname, nachname, email, telefon
3. Frontend POST /api/anmeldungen/ with course ID + participant data
4. Backend:
   a. Validate input (AnmeldungCreateSerializer)
   b. Check course exists and has capacity (ist_voll)
   c. get_or_create Teilnehmer by email
      → existing email = returning participant
      → new email = new participant created automatically
   d. Check no duplicate active enrollment
   e. Create Anmeldung with status='angemeldet'
5. Return 201 with enrollment data
6. Frontend shows success modal

Data Flow Diagram
Browser
  │
  │ HTTPS
  ▼
Traefik
  │
  ├─ /* ──────────────────► nginx container
  │                              │
  │                         serves static files
  │                         index.html
  │                         courses.html
  │                         course-detail.html
  │                         login.html
  │                         js/api.js ──────────────┐
  │                                                  │ XHR/fetch
  │                                                  ▼
  └─ /api/* ──────────────► Django (gunicorn)
  └─ /api-token-auth/* ──►      │
  └─ /admin/* ──────────►       │
                                ├─ Token Auth
                                ├─ kurse app
                                ├─ teilnehmer app
                                ├─ anmeldungen app
                                │
                                ▼
                           PostgreSQL
                           ├─ kurse
                           ├─ teilnehmer
                           └─ anmeldungen

Key Design Decisions
1. Token Authentication — simple stateless auth, token stored in localStorage. Not the most secure (vs httpOnly cookies) but straightforward for an API-first app.
2. get_or_create for participants — a participant is identified by email. If someone enrolls in two courses, they're the same Teilnehmer record. Smart but means email is the unique identifier.
3. Soft-delete enrollments — cancellations set status='storniert' instead of deleting the record. This preserves history and means verfuegbare_plaetze only counts status='angemeldet' rows.
4. Business logic in model — capacity checks and duplicate prevention live in Anmeldung.clean() AND in the view. Double validation — the model protects data integrity, the view gives better error messages.
5. Read-only courses — courses can only be created/edited via Django admin, not via API. The frontend is enrollment-only, not course management.

What's Missing for Production
FeatureCurrent StateWhat's NeededEmail confirmationNot implementedCelery + SMTPPassword resetNot implementedDjango allauth or customRate limitingNonedjango-ratelimitInput sanitizationBasicDRF validators sufficientLoggingBasic gunicornStructured logging to fileBackupsNonepg_dump cron jobAdmin notificationsNoneSignal on new enrollmentDu hast gesagt: can you describe how it works the system and key points to explain  because this just mvpcan you describe how it works the system and key points to explain  because this just mvp11:39 AMClaude hat geantwortet: Educore — How It Works (MVP)Educore — How It Works (MVP)

What It Does in One Sentence
Educore is a simple e-learning registration platform where an admin creates courses via Django admin, and users browse and enroll in them through a web frontend.

The Complete User Journey
As a visitor:
1. Land on educore.smarta.website
2. See featured courses on homepage (requires login)
3. Click "Anmelden" → redirected to login page
4. Enter credentials → get token → stored in browser
5. Browse courses, filter by availability
6. Click a course → see details, capacity bar
7. Click "Jetzt anmelden" → fill form → enrolled
8. Success modal confirms enrollment
As an admin:
1. Go to educore.smarta.website/admin/
2. Create courses (titel, dates, max_teilnehmer)
3. View all enrollments and participants
4. No code needed — pure Django admin UI

3 Core Concepts
1. Course Capacity
pythonverfuegbare_plaetze = max_teilnehmer - active_enrollments
ist_voll = verfuegbare_plaetze <= 0
Every time someone enrolls, available seats decrease. The frontend shows a live progress bar. When full, the enroll button disappears and shows "Ausgebucht".
2. Participant Identity
pythonteilnehmer, created = Teilnehmer.objects.get_or_create(
    email=data['email'],
    defaults={...}
)
Email is the unique identifier. The same person enrolling in multiple courses is one database record. A new email = new participant, automatically created at enrollment time. No registration required.
3. Token Authentication
Login → Django returns token → stored in localStorage
Every API call → sends "Authorization: Token abc123"
Logout → token deleted from localStorage
The token never expires in this MVP. Every page checks for a token on load — if missing, redirects to login.

Key Technical Points
Why Django REST Framework?
Simple, battle-tested, built-in token auth, automatic serialization, and browsable API via Swagger. For an MVP with 3 endpoints it's the right choice.
Why separate Frontend container?
The frontend is pure static files — no server-side rendering. nginx serves HTML/CSS/JS in microseconds. Django doesn't need to handle static file requests, keeping it focused on API logic.
Why PostgreSQL over SQLite?
Concurrent enrollments. SQLite locks the entire database on writes — if 10 people try to enroll simultaneously, 9 would fail. PostgreSQL handles concurrent writes gracefully with row-level locking.
The Double-Validation Pattern
View level  → fast check, returns good error messages to user
Model level → data integrity guarantee, last line of defense
Both check capacity and duplicates. The model's clean() runs on every save(), so even if someone bypasses the API and uses the admin panel, the rules still apply.

What Makes This MVP
FeatureMVP ApproachProduction Would AddAuthToken in localStoragehttpOnly cookies, refresh tokensEmailNo confirmation sentCelery + SMTP on enrollmentPaymentsNoneStripe integrationCourse contentTitle + description onlyVideos, PDFs, modulesUser profileNo dashboardMy enrollments pageAdmin alertsNoneEmail on new enrollmentToken expiryNever expiresExpiring tokens + refresh

The One Flow That Ties Everything Together
POST /api/anmeldungen/
        │
        ▼
AnmeldungCreateSerializer.validate()
  → course exists?
  → course full?
        │
        ▼
Teilnehmer.get_or_create(email)
  → returning user? reuse record
  → new user? create silently
        │
        ▼
Duplicate check
  → already enrolled with status='angemeldet'?
  → return 409 Conflict
        │
        ▼
Anmeldung.objects.create()
  → model.clean() runs again (safety net)
  → status = 'angemeldet'
        │
        ▼
Return 201 with enrollment data
This single endpoint handles the entire business logic of the platform. Everything else — courses listing, participant management — is supporting infrastructure for this one action.

In Short
Educore is intentionally simple: one admin creates courses, users enroll via a form, the system prevents overbooking and duplicate enrollments. The MVP proves the concept works end-to-end with real infrastructure (Docker, PostgreSQL, Traefik, SSL) — ready to extend with payments, email notifications, and user dashboards when needed.