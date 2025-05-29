from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def permission_required(perm_code):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(perm_code):
                return Response(
                    {"detail": "No tienes permiso para realizar esta acción."},
                    status=status.HTTP_403_FORBIDDEN
                )
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator