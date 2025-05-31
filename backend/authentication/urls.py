from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, RegisterView, UserProfileView, GoogleAuthTokenView, AdminUserCreateView

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('google/', GoogleAuthTokenView.as_view(), name='google_login'),
    path('admin/create-user/', AdminUserCreateView.as_view(), name='admin_create_user'),
]