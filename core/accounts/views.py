from accounts.forms import CustomRegisterForm, CustomLoginForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from accounts.tasks import send_mail_task
import requests

class RegisterView(CreateView):
    form_class = CustomRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "registration/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("blog:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def send_mail(request):
    send_mail_task.delay()
    return JsonResponse({"status": "ok"})

@cache_page(60 * 5)
def test(request):
    response = requests.get("https://5584d8b6-3f5f-4993-ac9d-534c2ae2bd1b.mock.pstmn.io/test/delay/5/")  
    return JsonResponse(response.json())
