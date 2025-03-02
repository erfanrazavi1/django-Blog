from django.urls import path
from blog.views import (
    HomeView,
    PostListView,
    PostDetailView,
    CategoryPostListView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
    )

app_name = 'blog'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('post-list/', PostListView.as_view(), name='post-list'),
    path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path("category/<int:category_id>/", CategoryPostListView.as_view(), name="category-posts"),
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("update/<int:pk>/", UpdatePostView.as_view(), name="update-post"),
    path("delete/<int:pk>/", DeletePostView.as_view(), name="delete-post"),

]