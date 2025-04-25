from django.urls import path, include
from accounts.views import RegisterView, CustomLoginView, CustomLogoutView, send_mail


from django.urls import reverse_lazy


app_name = "accounts"

urlpatterns = [
    path("send-mail/", send_mail, name="send_mail"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path(
        "logout/",
        CustomLogoutView.as_view(next_page=reverse_lazy("blog:index")),
        name="logout",
    ),
    path("accounts/api/v1/", include("accounts.api.v1.urls")),
]
