### STAGE 1: Build ###
FROM node:12.7-alpine AS build
WORKDIR /usr/src/app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run-script build

### STAGE 2: Run ###
FROM caddy:2.4.6
COPY ./Caddyfile /etc/caddy/Caddyfile
COPY ./index.html /srv/index.html
COPY ./styles.css /srv/styles.css
COPY ./favicon.ico /srv/favicon.ico
COPY --from=build /usr/src/app/bin /srv/bin
