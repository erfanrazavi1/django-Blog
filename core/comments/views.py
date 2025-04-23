# from django.views.generic import CreateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from comments.forms import CommentForm
# from blog.models import Post
# from comments.models import Comment
# from django.shortcuts import get_object_or_404

# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     template_name = "blog/post_detail.html"
#     form_class = CommentForm
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
#         return super().form_valid(form)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = CommentForm()
#         return context  