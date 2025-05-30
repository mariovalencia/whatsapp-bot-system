from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from security.models import UserRole, RolePermission
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_verified']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_verified'] = user.is_verified
        
         # Roles y permisos del usuario
        roles = UserRole.objects.filter(user=user).select_related('role')
        token['roles'] = [user_role.role.name for user_role in roles]
        
        # Permisos únicos (evitando duplicados si un rol tiene múltiples permisos)
        permissions = set()
        for role in roles:
            perms = RolePermission.objects.filter(role=role.role).select_related('permission')
            permissions.update([perm.permission.code for perm in perms])
        token['permissions'] = list(permissions)
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
    
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=None  # Sin contraseña para login solo con Google
        )
        return user