from django.urls import path
from accounts.api.v1.views import (
    ProfileApiView,
)


urlpatterns = [
    path("", ProfileApiView.as_view(), name="profile"),
]
