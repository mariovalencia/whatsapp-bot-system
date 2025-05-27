from rest_framework import viewsets
from .models import Role, Permission, UserRole
from .serializers import RoleSerializer, PermissionSerializer, UserRoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer