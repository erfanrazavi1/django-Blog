from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.api.v1.views import PostListViewSet

app_name = 'api-v1'
router = DefaultRouter()
router.register('post', PostListViewSet, basename='post')

urlpatterns = router.urls

