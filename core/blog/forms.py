from django import forms
from blog.models.posts import Post

class PostForm(forms.ModelForm):
    """Form for creating and updating posts."""

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
        ]