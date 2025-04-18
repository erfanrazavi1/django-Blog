from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from blog.models import Post, Category
from django.contrib.auth.models import Permission


class TestBlogViews(TestCase):
   
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email="erfan@gmail.com",
            phone="09123456789",
            password="password123",
            is_staff=True
            )
        """
            Granting the required permission to the test user.
            The `CreatePostView` uses `PostPermissionMixin`, which checks if the user:
            1. Is authenticated
            2. Is marked as staff (`is_staff=True`)
            3. Has the `blog.add_post` permission
            We manually assign the permission here to ensure the user passes the view's access control.
        """
        permission = Permission.objects.get(codename='add_post')
        self.user.user_permissions.add(permission)
        self.profile = self.user.profile
        self.category = Category.objects.create(name="Test Category")

    def test_blog_index_url_response_200(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
    
    def test_blog_post_create_with_logged_in_user(self):
        self.client.force_login(self.user)
        url = reverse('blog:create-post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_blog_post_create_with_logged_out_user(self):
        url = reverse('blog:create-post')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    
    
    
