from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from security.models import UserRole, RolePermission

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