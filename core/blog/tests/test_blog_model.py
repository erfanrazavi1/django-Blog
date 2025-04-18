from django.test import TestCase
from blog.models import Post, Category
from accounts.models import CustomUser


class TestPostModel(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email = "erfan@gmail.com",
            phone = "09123456789",
            password = "password123",
        )
        self.profile = self.user.profile
        self.category = Category.objects.create(name="Test Category")
    
    def test_post_creation(self):
        post = Post.objects.create(
            author=self.profile,
            title="Test Title",
            content="Test Content",
            status=True,
            category=self.category,
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.content, "Test Content")
        self.assertEqual(post.status, True)
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.author, self.profile)
    
    def test_post_str_method(self):
        post = Post.objects.create(
            author=self.profile,
            title="Test Title",
            content="Test Content",
            status=True,
            category=self.category,
        )
        self.assertEqual(str(post), "Test Title")

