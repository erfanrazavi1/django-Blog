from django.urls import path, include

urlpatterns = [
    path("", include("blog.api.v1.urls.post")),
]
