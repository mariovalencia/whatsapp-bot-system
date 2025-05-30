import os
import logging
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import MyTokenObtainPairSerializer, UserSerializer, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from security.decorators import permission_required
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialApp

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    @permission_required('admin.access')
    def get(self, request):
        return Response({"data": "Solo para admins"})
    
# Configuración del logger
logger = logging.getLogger(__name__)

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('GOOGLE_CALLBACK_URL')  # Ej: http://localhost:3000/callback
    client_class = OAuth2Client
    
    def post(self, request, *args, **kwargs):
        try:
            # 1. Validar token
            token = request.data.get('token')
            if not token:
                return Response(
                    {"error": "Token de Google requerido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Extraer email del token (sin autenticar)
            from allauth.socialaccount.providers.google import views as google_views
            adapter = self.adapter_class(request)
            provider = adapter.get_provider()
            login = provider.sociallogin_from_response(request, {'id_token': token})
            email = login.user.email

            # 3. Verificar si el usuario existe
            user_exists = User.objects.filter(email=email).exists()

            # 4. Modo seguro: Si requiere pre-registro y no existe
            if not user_exists and os.getenv('REQUIRE_PRE_REGISTER', 'False') == 'True':
                return Response(
                    {
                        "error": "Usuario no registrado",
                        "detail": "El administrador debe registrar este correo primero",
                        "email": email
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # 5. Procesar autenticación
            request.data.update({
                'access_token': token,
                'id_token': token,
                'code': '',
                'provider': 'google'
            })

            response = super().post(request, *args, **kwargs)

            if not request.user.is_authenticated:
                return Response(
                    {"error": "Falló la autenticación"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return response

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
class AdminUserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser]