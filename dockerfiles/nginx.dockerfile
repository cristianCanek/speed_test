FROM nginx:1.29.0-alpine3.22-slim

WORKDIR /etc/nginx/conf.d

COPY config_files/nginx.conf default.conf