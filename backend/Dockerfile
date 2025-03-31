FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto para el servidor
EXPOSE 8000

# Comando por defecto(Se sobrescribe en docker-compose)
CMD [ "gunicorn","core.wsgi:application","--bind","0.0.0.0:8000" ]