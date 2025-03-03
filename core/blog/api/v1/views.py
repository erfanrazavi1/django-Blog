from rest_framework.response import Response
from blog.api.v1.serializer import PostListSerializer, CategorySerializer
from blog.models import Post, Category
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from blog.api.v1.permissions import IsOwnerOrReadOnly
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.api.v1.pagination import CustomPagination



class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=True).order_by('-created_date')
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomPagination

    filterset_fields = {
        "category": ["exact", "in"],
        "status": ["exact", "in"],
        "author": ["exact", "in"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["-title", "id", "published_date"]


    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.views = F('views') + 1
        post.save()
        post.refresh_from_db()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)
        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthenticated]
    pagination_class = CustomPagination
    search_fields = ["name"]
    ordering_fields = ["name"]
    filterset_fields = {
        "name": ["exact", "in"],
    }

    