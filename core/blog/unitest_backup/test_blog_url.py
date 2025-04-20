# from django.test import TestCase
# from django.urls import reverse
# from django.urls import resolve
# from blog.views import HomeView, PostListView, PostDetailView


# class TestUrl(TestCase):
#     def test_blog_index_url_resolves(self):
#         url = reverse('blog:index')
#         self.assertEqual(resolve(url).func.view_class, HomeView)

#     def test_blog_post_list_url_resolves(self):
#         url = reverse('blog:post-list')
#         self.assertEqual(resolve(url).func.view_class, PostListView)

#     def test_blog_post_detail_url_resolves(self):
#         url = reverse('blog:post-detail', kwargs={'pk': 3})
#         self.assertEqual(resolve(url).func.view_class, PostDetailView)
