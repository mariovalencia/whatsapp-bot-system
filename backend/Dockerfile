FROM python:3.10.12-slim-bullseye

WORKDIR /app

# Instalar dependencias del sistema (incluyendo netcat)
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 2; done && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]