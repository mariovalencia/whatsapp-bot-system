from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

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