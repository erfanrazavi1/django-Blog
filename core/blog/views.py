from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import F
from blog.models import Post, Category

class HomeView(TemplateView):
    """
    a class based view to show index page
    """
    template_name = 'blog/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(status=True)
        return context

class PostListView(ListView):
    """
    a class based view to show all posts
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_date']
    def get_queryset(self):
        return Post.objects.filter(status=True).order_by('-created_date')

class PostDetailView(DetailView):
    """
    a class based view to show post detail
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    def get_object(self):
        post = super().get_object()
        Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
        post.refresh_from_db()
        return post


class CategoryPostListView(ListView):
    """
    a class based view to show posts by category
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Post.objects.filter(category_id=category_id, status=True).order_by('-created_date')

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'content', 'category']
    login_url = reverse_lazy('accounts:login') 

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

        form.instance.author = self.request.user.profile

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def get_success_url(self):
        return reverse_lazy('blog:post-list')





