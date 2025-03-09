from django.urls import path
from accounts.api.v1.views import RegisterApiView, CustomObtainAuthToken, CustomLogoutView
from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'accounts-api-v1'

urlpatterns = [
    path('registration/', RegisterApiView.as_view(), name='registration'),

    # token authentication
    path('token/login/', CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('token/logout/', CustomLogoutView.as_view(), name='logout'),

]
