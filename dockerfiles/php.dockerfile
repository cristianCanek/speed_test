FROM php:8.4.10-fpm-alpine3.22

WORKDIR /app/public

# PHP keeps serving the same frontend/backend files used by Version 1.
COPY web_page .
