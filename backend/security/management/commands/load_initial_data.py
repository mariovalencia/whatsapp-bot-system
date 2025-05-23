from django.core.management.base import BaseCommand
from security.models import Role, Permission, RolePermission, UserRole
from authentication.models import User

class Command(BaseCommand):
    help = 'Carga datos iniciales para el sistema'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Cargando datos iniciales...'))
        
        # Crear roles
        admin_role, _ = Role.objects.get_or_create(name='admin', description='Administrador del sistema')
        technician_role, _ = Role.objects.get_or_create(name='technician', description='Técnico de soporte')
        client_role, _ = Role.objects.get_or_create(name='client', description='Cliente')
        
        # Crear permisos
        permissions = [
            {'code': 'view_dashboard', 'name': 'Ver dashboard', 'description': 'Permiso para ver el dashboard'},
            {'code': 'manage_users', 'name': 'Gestionar usuarios', 'description': 'Permiso para gestionar usuarios'},
            {'code': 'manage_bot', 'name': 'Gestionar bot', 'description': 'Permiso para gestionar el bot'},
            {'code': 'view_chats', 'name': 'Ver chats', 'description': 'Permiso para ver los chats'},
            {'code': 'take_chats', 'name': 'Tomar chats', 'description': 'Permiso para tomar chats de clientes'},
        ]
        
        for perm_data in permissions:
            perm, _ = Permission.objects.get_or_create(**perm_data)
            
            # Asignar permisos a roles
            if perm.code in ['view_dashboard', 'manage_users', 'manage_bot', 'view_chats']:
                RolePermission.objects.get_or_create(role=admin_role, permission=perm)
            
            if perm.code in ['view_dashboard', 'view_chats', 'take_chats']:
                RolePermission.objects.get_or_create(role=technician_role, permission=perm)
            
            if perm.code == 'view_dashboard':
                RolePermission.objects.get_or_create(role=client_role, permission=perm)
        
        # Crear usuario admin si no existe
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_verified=True
            )
            UserRole.objects.create(user=admin, role=admin_role)
            self.stdout.write(self.style.SUCCESS('Usuario admin creado: admin@example.com / admin123'))
        
        self.stdout.write(self.style.SUCCESS('Datos iniciales cargados correctamente'))