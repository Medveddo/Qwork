### STAGE 1: Build ###
FROM node:18-alpine AS build

WORKDIR /usr/src/app
COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . .

ARG VITE_API_URL
ARG VITE_ENVIRONMENT

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_ENVIRONMENT=$VITE_ENVIRONMENT

RUN npm run build

### STAGE 2: Run ###
FROM caddy:2.4.6
COPY --from=build /usr/src/app/build /srv
