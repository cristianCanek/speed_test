FROM nginx:1.29.0-alpine3.22-slim

WORKDIR /etc/nginx/conf.d

COPY config_files/nginx.conf default.conf

# Nginx must have local access to static frontend assets, including Chart.js.
COPY web_page /app/public
