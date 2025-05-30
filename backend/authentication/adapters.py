from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """
        Permite registro solo si el email ya existe en la base de datos
        o si está permitido el auto-registro
        """
        if request.path == '/api/auth/google/':
            return True  # Permite auto-registro para Google
        return super().is_open_for_signup(request)