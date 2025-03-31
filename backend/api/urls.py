from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from authentication.views import RegisterView, LoginView, UserProfileView
from security.views import RoleViewSet, UserRoleViewSet, PermissionViewSet
from bot_management.views import CategoryViewSet, QuestionAnswerViewSet, AlternativeQuestionViewSet
from whatsapp_integration.views import WhatsAppSessionViewSet, ContactViewSet, ConversationViewSet, MessageViewSet

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

# Crear el router para las APIs
router = DefaultRouter()

# Rutas para seguridad y roles
router.register(r'roles', RoleViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'permissions', PermissionViewSet)

# Rutas para gestión del bot
router.register(r'categories', CategoryViewSet)
router.register(r'questions', QuestionAnswerViewSet)
router.register(r'alternatives', AlternativeQuestionViewSet)

# Rutas para integración de WhatsApp
router.register(r'whatsapp-sessions', WhatsAppSessionViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    # Autenticación
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    
    # APIs usando router
    path('', include(router.urls)),
]

