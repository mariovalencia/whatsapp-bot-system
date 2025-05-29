from django.http import JsonResponse

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return self.get_response(request)

        required_permission = getattr(request.resolver_match.func, 'permission', None)
        if required_permission and not request.user.has_perm(required_permission):
            return JsonResponse({'error': 'Forbidden'}, status=403)

        return self.get_response(request)