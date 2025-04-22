from django.urls import path, include
from blog.views import (
    HomeView,
    PostListView,
    PostDetailView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
    PostListApiView,
)

app_name = "blog"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("post-list/", PostListView.as_view(), name="post-list"),
    path("post/api/", PostListApiView.as_view(), name="post-list-api"),
    path("post-detail/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("update/<int:pk>/", UpdatePostView.as_view(), name="update-post"),
    path("delete/<int:pk>/", DeletePostView.as_view(), name="delete-post"),
    path("blog/api/v1/", include("blog.api.v1.urls")),
]
