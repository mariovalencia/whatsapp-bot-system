import os
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from security.decorators import permission_required
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

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
    
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = os.getenv('GOOGLE_CALLBACK_URL')  # Ej: http://localhost:3000/callback
    client_class = OAuth2Client