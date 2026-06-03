Here's a practical deployment guide based on everything we went through:

Deploying Frontend + Backend on Coolify with Traefik
Architecture to Use
Internet → Traefik → /api/* → Backend (Django/Node/etc)
                   → /*     → Frontend (nginx/static)

Step 1: Project Structure
project/
├── docker-compose.yaml    # NO version: field
├── frontend/
│   └── Dockerfile         # FROM nginx:alpine, EXPOSE 80
└── backend/
    └── Dockerfile         # Never run collectstatic/build at image build time

Step 2: Dockerfile Rules
Backend — never use secrets at build time:
dockerfile# WRONG - fails because SECRET_KEY not available during build
RUN python manage.py collectstatic --noinput

# CORRECT - run at container startup when env vars exist
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn ..."]
Frontend:
dockerfileFROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80

Step 3: Coolify Settings (do this BEFORE writing labels)
In Coolify UI → Advanced:

✅ Enable "Raw Compose Deployment" — stops Coolify injecting conflicting labels
✅ Clear all domain fields in General — let docker-compose handle routing
✅ Set all secrets in Environment Variables tab, not in docker-compose


Step 4: docker-compose.yaml Template
yamlservices:
  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal

  backend:
    build:
      context: ./backend
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      - DB_HOST=postgres
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - SECRET_KEY=${SECRET_KEY}
    networks:
      - internal
      - coolify              # shares network with Traefik
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=coolify"
      - "traefik.http.routers.myapp-backend.rule=Host(`myapp.example.com`) && (PathPrefix(`/api/`) || PathPrefix(`/admin/`))"
      - "traefik.http.routers.myapp-backend.entryPoints=https"
      - "traefik.http.routers.myapp-backend.tls=true"
      - "traefik.http.routers.myapp-backend.tls.certresolver=letsencrypt"
      - "traefik.http.routers.myapp-backend.priority=100"
      - "traefik.http.routers.myapp-backend.service=myapp-backend"
      - "traefik.http.services.myapp-backend.loadbalancer.server.port=8100"

  frontend:
    build:
      context: ./frontend
    restart: unless-stopped
    networks:
      - coolify              # shares network with Traefik
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=coolify"
      - "traefik.http.routers.myapp-frontend.rule=Host(`myapp.example.com`)"
      - "traefik.http.routers.myapp-frontend.entryPoints=https"
      - "traefik.http.routers.myapp-frontend.tls=true"
      - "traefik.http.routers.myapp-frontend.tls.certresolver=letsencrypt"
      - "traefik.http.routers.myapp-frontend.priority=1"
      - "traefik.http.routers.myapp-frontend.service=myapp-frontend"
      - "traefik.http.services.myapp-frontend.loadbalancer.server.port=80"
      - "traefik.http.routers.myapp-frontend-http.rule=Host(`myapp.example.com`)"
      - "traefik.http.routers.myapp-frontend-http.entryPoints=http"
      - "traefik.http.routers.myapp-frontend-http.middlewares=redirect-to-https"
      - "traefik.http.routers.myapp-frontend-http.service=myapp-frontend"
      - "traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https"

networks:
  internal:
    driver: bridge         # backend ↔ postgres only, Traefik never needs this
  coolify:
    external: true         # Traefik's network

volumes:
  postgres_data:

Step 5: DNS & SSL Checklist
bash# 1. Verify DNS resolves BEFORE deploying
dig myapp.example.com A

# 2. After deploy, check cert was issued
docker logs coolify-proxy 2>&1 | grep -i "obtained\|myapp"

# 3. Test HTTP redirect works
curl -I http://myapp.example.com

# 4. Test HTTPS backend directly
curl -sk https://myapp.example.com/api/health/

Step 6: Debugging Order (when things break)
bash# 1. Are containers running?
docker ps | grep myapp

# 2. Check container labels (are they what you expect?)
docker inspect <container_id> | python3 -c "
import json,sys; d=json.load(sys.stdin)
labels=d[0]['Config']['Labels']
[print(k,'=',v) for k,v in labels.items() if 'traefik' in k]"

# 3. Are backend/frontend on the coolify network?
docker inspect <container_id> --format='{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'

# 4. Can Traefik reach the container directly?
docker exec coolify-proxy wget -qO- http://<container_ip>:<port>/

# 5. Check SSL cert status
cat /data/coolify/proxy/acme.json | python3 -c "
import json,sys; d=json.load(sys.stdin)
certs=d.get('letsencrypt',{}).get('Certificates') or []
[print(c['domain']['main']) for c in certs]"

What to Avoid
❌ Avoid✅ Do Insteadversion: '3.8' in composeRemove it entirelycollectstatic in Dockerfile RUN Move to CMD at startupCoolify domain fields + custom labelsPick one — Raw Compose OR Coolify UI All services on one networkinternal for DB, coolify for public servicesMissing traefik.docker.network labelAlways specify which network Traefik should useSame priority on conflicting routesBackend=100, Frontend=1Missing .service label on routersAlways link router → service explicitlyWiping acme.json without backupAlways cp acme.json acme.json.bak first
The single most important label you were missing throughout was traefik.docker.network=coolify — when a container is on multiple networks, Traefik doesn't know which one to use without this hint.