FROM node:18-alpine

WORKDIR /app

# Instalar dependencias
COPY package.json package-lock.json* ./
RUN npm install

# Copiar el resto del código
COPY . .

# Puerto para desarrollo
EXPOSE 3000

# Comando por defecto
CMD ["npm", "start"]