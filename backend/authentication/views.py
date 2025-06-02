import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework import status, generics
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer, UserSerializer, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from security.decorators import permission_required


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Obtener el usuario del serializer después de la autenticación
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            
            # Asegúrate que todos los datos sean serializables
            roles = list(user.userrole_set.values_list('role__name', flat=True)) if hasattr(user, 'userrole_set') else []
            
            # Obtener permisos de forma serializable
            permissions = []
            if hasattr(user, 'userrole_set'):
                for role in user.userrole_set.all():
                    perms = role.role.rolepermission_set.values_list('permission__code', flat=True)
                    permissions.extend(list(perms))

            # Estructura estándar que espera el frontend
            response.data = {
                'access': response.data.get('access'),
                'refresh': response.data.get('refresh'),
                'user': UserSerializer(user).data,
                'roles': roles,  # Tus roles
                'permissions': list(set(permissions))  # Tus permisos
            }
        return response

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
    
User = get_user_model()

class GoogleAuthTokenView(APIView):
    def post(self, request):
        token = request.data.get('access_token')
        if not token:
            return Response({"error": "Token requerido"}, status=400)

        try:
            # Desactiva temporalmente la verificación de tiempo
            class CustomRequest(google_requests.Request):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._timeout = 30  # Aumenta timeout

            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id'],
                clock_skew_in_seconds=300
            )

            email = idinfo['email']
            name = idinfo.get('name', '')
            sub = idinfo.get('sub')

            if not email:
                return Response({"error": "Token no contiene email"}, status=400)

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': name,
                    'is_verified': True,
                }
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })

        except ValueError as e:
            return Response({"error": f"Token inválido: {e}"}, status=400)
        except Exception as e:
            import traceback
            return Response({
                "error": repr(e),
                "trace": traceback.format_exc()
            }, status=500)


            
class AdminUserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser]