from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    )

from blog.models import Post

class HomeView(TemplateView):
    """
    a class based view to show index page
    """
    template_name = 'blog/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

class PostListView(ListView):
    """
    a class based view to show all posts
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_date']

class PostDetailView(DetailView):
    """
    a class based view to show post detail
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    def get_object(self):
        post = super().get_object()
        post.views += 1 
        post.save(update_fields=['views'])  
        return post




