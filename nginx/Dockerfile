FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/

# Crear directorios para archivos estáticos y media
RUN mkdir -p /var/www/static /var/www/media

EXPOSE 80

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]