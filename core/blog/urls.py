from django.urls import path
from blog.views import login

urlpatterns = [
    path('', login, name='index')
]
