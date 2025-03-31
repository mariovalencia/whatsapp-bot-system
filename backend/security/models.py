from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    """Modelo para gestionar roles de usuario"""
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('supervisor', 'Supervisor'),
        ('tech', 'Técnico'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_name_display()

class UserRole(models.Model):
    """Asignación de roles a usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.username} - {self.role.get_name_display()}"

class Permission(models.Model):
    """Permisos específicos del sistema"""
    PERMISSION_CHOICES = [
        ('manage_users', 'Gestionar usuarios'),
        ('manage_bot', 'Gestionar configuración del bot'),
        ('answer_chats', 'Responder conversaciones'),
        ('view_reports', 'Ver reportes'),
        ('manage_whatsapp', 'Gestionar conexión WhatsApp'),
    ]
    
    name = models.CharField(max_length=50, choices=PERMISSION_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()

class RolePermission(models.Model):
    """Asignación de permisos a roles"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('role', 'permission')
    
    def __str__(self):
        return f"{self.role.get_name_display()} - {self.permission.get_name_display()}"