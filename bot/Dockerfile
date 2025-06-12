# bot/venom/Dockerfile
FROM node:18

# Instalar dependencias del sistema para Puppeteer (Chromium)
RUN apt-get update && apt-get install -y \
  wget \
  ca-certificates \
  fonts-liberation \
  libappindicator3-1 \
  libasound2 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libcups2 \
  libdbus-1-3 \
  libgdk-pixbuf2.0-0 \
  libnspr4 \
  libnss3 \
  libx11-xcb1 \
  libxcomposite1 \
  libxdamage1 \
  libxrandr2 \
  xdg-utils \
  libgbm-dev \
  libxshmfence-dev \
  libglu1-mesa \
  --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Crear y movernos al directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY package.json ./
RUN npm install

# Copiar el resto de la app
COPY . .

# Entrypoint
CMD ["node", "index.js"]
