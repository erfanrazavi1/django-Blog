from rest_framework import generics
from accounts.models import CustomUser
from accounts.api.v1.serializer import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
