from django.urls import path
from accounts.api.v1.views import (
    RegisterApiView,
    CustomObtainAuthToken,
    CustomLogoutView,
    CustomTokenObtainPairView,
    ChangePasswordApiView,
    TestEmailSend,
    ActivationConfirmEmailView,
    ActivationResendEmailView,
    ResetPasswordEmailView,
    SetNewPasswordView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("registration/", RegisterApiView.as_view(), name="registration"),
    # activation
    path("test-email/", TestEmailSend.as_view(), name="test-email"),
    path(
        "activation/confirm/<str:token>",
        ActivationConfirmEmailView.as_view(),
        name="activation",
    ),
    path(
        "activation/resend/",
        ActivationResendEmailView.as_view(),
        name="activate",
    ),
    # reset pass
    path(
        "password/reset/",
        ResetPasswordEmailView.as_view(),
        name="reset-password",
    ),
    path(
        "password/reset/confirm/<str:token>/",
        SetNewPasswordView.as_view(),
        name="password-reset-confirm",
    ),
    # token authentication
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", CustomLogoutView.as_view(), name="token-logout"),
    # change password
    path(
        "change-password/",
        ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # jwt authentication
    path(
        "jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
