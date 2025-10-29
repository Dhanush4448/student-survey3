FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY ./config-runtime.sh /docker-entrypoint.d/50-config-runtime.sh
RUN chmod +x /docker-entrypoint.d/50-config-runtime.sh
EXPOSE 80
