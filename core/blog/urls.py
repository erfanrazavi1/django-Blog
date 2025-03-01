from django.urls import path
from blog.views import HomeView, PostListView, PostDetailView, CategoryPostListView, CreatePostView

app_name = 'blog'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('post-list/', PostListView.as_view(), name='post-list'),
    path('post-detail/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path("category/<int:category_id>/", CategoryPostListView.as_view(), name="category-posts"),
    path("create/", CreatePostView.as_view(), name="create-post"),

]