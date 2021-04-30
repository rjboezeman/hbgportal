# Production stage
FROM nginx:latest as production-stage
COPY ./nginx.conf /etc/nginx/nginx.conf
