from django.urls import path
from accounts.api.v1.views import RegisterUserView

urlpatterns = [
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
]