from django.urls import path
from accounts.api.v1.views import RegisterApiView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
