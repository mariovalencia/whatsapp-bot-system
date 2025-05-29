from security.models import Role, UserRole

def assign_default_role(sociallogin, **kwargs):
    user = sociallogin.user
    if not UserRole.objects.filter(user=user).exists():
        default_role = Role.objects.get(name='cliente')
        UserRole.objects.create(user=user, role=default_role)