CREATE DATABASE whatsapp_bot;
CREATE USER bot_django_user WITH PASSWORD 'django_password_456';
CREATE USER bot_node_user WITH PASSWORD 'node_password_789';

GRANT ALL PRIVILEGES ON DATABASE whatsapp_bot TO bot_django_user;
ALTER DATABASE whatsapp_bot OWNER TO bot_django_user;

-- Si el bot necesita permisos específicos
GRANT CONNECT ON DATABASE whatsapp_bot TO bot_node_user;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO bot_node_user;