from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import LogoutView, register_user, user_profile, list_users


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='auth_logout'),

    path('api/users/register/', register_user, name='register'),
    path('api/users/profile/', user_profile, name='profile'),

    path('api/users/', list_users, name='list_users')
]