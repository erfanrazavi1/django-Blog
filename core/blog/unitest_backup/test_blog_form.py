# from django.test import TestCase
# from blog.forms import PostForm
# from blog.models.category import Category

# class TestPostForm(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name="Test Category")

#     def test_post_form_valid_data(self):
#         form = PostForm(data={
#             "title": "Test Title",
#             "content": "Test Content",
#             "category":self.category ,  # Assuming category with ID 1 exists
#         })
#         self.assertTrue(form.is_valid())

#     def test_post_form_valid_no_data(self):
#         form = PostForm(data={})
#         self.assertFalse(form.is_valid())
