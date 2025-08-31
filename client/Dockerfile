# syntax=docker/dockerfile:1

FROM node:20 AS build
WORKDIR /app


ARG VITE_BACKEND_BASE_URL
ARG VITE_BACKEND_URL
ARG VITE_SIGNUP_URL
ARG VITE_LOGIN_URL
ARG VITE_REFRESH_TOKEN_URL
ARG VITE_LOGOUT_URL

COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# Set environment variables for Vite build
ENV VITE_BACKEND_BASE_URL=$VITE_BACKEND_BASE_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
ENV VITE_SIGNUP_URL=$VITE_SIGNUP_URL
ENV VITE_LOGIN_URL=$VITE_LOGIN_URL
ENV VITE_REFRESH_TOKEN_URL=$VITE_REFRESH_TOKEN_URL
ENV VITE_LOGOUT_URL=$VITE_LOGOUT_URL

RUN npm run build

# Production stage
FROM nginx:1.25-alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 