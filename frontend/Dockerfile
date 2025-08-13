# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build

# Run stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Route /api/* to backend (api:5000) via Nginx
RUN sed -i 's|try_files \$uri \$uri/ /index.html;|try_files \$uri \$uri/ /index.html;|' /etc/nginx/conf.d/default.conf \
 && printf "\nlocation /api/ {\n  proxy_pass http://api:5000/;\n  proxy_set_header Host \$host;\n}\n" >> /etc/nginx/conf.d/default.conf
EXPOSE 80
