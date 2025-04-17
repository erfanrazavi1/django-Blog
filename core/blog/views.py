from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.shortcuts import redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse, reverse_lazy
from django.db.models import F
from blog.models import Post, Category


class HomeView(TemplateView):
    """Show index page."""

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(status=True)
        return context


class PostListView(ListView):
    """Show all posts."""

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(status=True).order_by("-created_date")


class PostDetailView(DetailView):
    """Show post detail."""

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self):
        post = super().get_object()
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
        post.refresh_from_db()
        return post


class PostPermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Mixin to check permission for Post views."""

    login_url = reverse_lazy("accounts:login")

    def has_permission(self):
        return (
            self.request.user.is_active
            and self.request.user.is_staff
            and super().has_permission()
        )

    def handle_no_permission(self):
        return redirect("accounts:login")


class CreatePostView(PostPermissionMixin, CreateView):
    model = Post
    template_name = "blog/create_post.html"
    fields = ["title", "content", "category"]
    permission_required = "blog.add_post"

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})


class UpdatePostView(PostPermissionMixin, UpdateView):
    model = Post
    template_name = "blog/update_post.html"
    fields = ["title", "content", "category"]
    permission_required = "blog.change_post"

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user.profile, status=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy("blog:post-list")


class DeletePostView(PostPermissionMixin, DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("blog:post-list")
    permission_required = "blog.delete_post"

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user.profile, status=True
        )
