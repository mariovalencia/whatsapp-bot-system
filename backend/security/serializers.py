from rest_framework import serializers
from .models import Role, Permission, UserRole

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions']

class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']