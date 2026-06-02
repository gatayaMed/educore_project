# frontend/Dockerfile
FROM nginx:alpine

# Copy static files to nginx serve directory
COPY . /usr/share/nginx/html

# Expose port 80 (standard HTTP port)
# Coolify/Traefik will handle SSL and routing
EXPOSE 80

# Nginx starts automatically
# No custom CMD needed