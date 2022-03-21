### STAGE 1: Build ###
FROM node:14.13-alpine AS build
WORKDIR /usr/src/app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

### STAGE 2: Run ###
FROM caddy:2.4.6
COPY ./Caddyfile /etc/caddy/Caddyfile
COPY --from=build /usr/src/app/build /srv
