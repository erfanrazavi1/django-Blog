from django.urls import path
from accounts.api.v1.views import (
    RegisterApiView,
    CustomObtainAuthToken,
    CustomLogoutView,
    CustomTokenObtainPairView,
    ChangePasswordApiView,
    ProfileApiView,
    )
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    
    )

app_name = 'accounts-api-v1'

urlpatterns = [
    path('registration/', RegisterApiView.as_view(), name='registration'),

    # token authentication
    path('token/login/', CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', CustomLogoutView.as_view(), name='token-logout'),

    # change password
    path('change-password/', ChangePasswordApiView.as_view(), name='change-password'),

    # jwt authentication
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

    path('profile/', ProfileApiView.as_view(), name='profile'),


]
