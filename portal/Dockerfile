# Develop stage
FROM node:latest as develop-stage
WORKDIR /portal
COPY package*.json ./
RUN npm install -g @quasar/cli
COPY . .

# # Build stage
# FROM develop-stage as build-stage
# RUN yarn
# RUN quasar build

# # Production stage
# FROM nginx:latest as production-stage
# COPY --from=build-stage /portal/dist/spa /var/www/html
# COPY ./nginx.conf /etc/nginx/nginx.conf
