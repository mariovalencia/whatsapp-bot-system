from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import(
    UserViewSet,RoleViewSet,PermissionViewSet,
    CategoryViewSet,QuestionAnswerViewSet,
    WhatsAppSessionViewSet, ContactViewSet, ConversationViewSet
)

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="WhatsApp Bot API",
        default_version='v1',
        description="API para sistema de bot de WhatsApp con interfaz Web",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

# Configuración de router para las vistas basadas en viewsets
router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'questions', QuestionAnswerViewSet)
router.register(r'whatsapp-sessions', WhatsAppSessionViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    # Rutas de la API
    path('', include(router.urls)),

    # Rutas de la autenticación
    path('auth/', include('authentication.urls')),

    # Documentación Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

