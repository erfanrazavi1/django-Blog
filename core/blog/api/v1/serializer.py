from rest_framework import serializers
from blog.models import Post, Category
from django.urls import reverse
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='name',
        queryset=Category.objects.all()
    )
    author = serializers.SlugRelatedField(
    slug_field="user__email", queryset=Profile.objects.all()
    )
    class Meta:
        model = Post
        fields = ["id", "title", "content", "category", "author", "detail_url", "created_date", "published_date"]
        read_only_fields = ['author', 'created_date', 'published_date']

    def get_detail_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context["kwargs"].get("pk"):
            rep.pop("detail_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data  # When we want to call the serializer elsewhere,
        # we pass the request along with it

        return rep
