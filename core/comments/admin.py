from django.contrib import admin
from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "content", "created_at", "is_active")
    search_fields = ("user__username", "post__title", "content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
