from django.urls import path
from rest_framework import routers
from .views import RoleViewSet, PermissionViewSet

router = routers.DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = router.urls