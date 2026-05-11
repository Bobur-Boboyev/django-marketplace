from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import LogoutView, register_user, user_profile, list_users


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("users/register/", register_user, name="register"),
    path("users/profile/", user_profile, name="profile"),
    path("users/", list_users, name="list_users"),
]
