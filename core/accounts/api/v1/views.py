from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response     
from accounts.api.v1.serializer import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordApiSerializer,
    ProfileSerializer,
    )
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from accounts.api.utils import EmailThread
from django.core.mail import EmailMessage

User = get_user_model()


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
            
        data = {
            'email': user.email,
            'phone': user.phone,
            'detail': 'User registered successfully'
        }
        return Response(data, status=status.HTTP_201_CREATED)
    


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist:
            return Response({"error": "Token not found"}, status=400)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    serializer_class = ChangePasswordApiSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj



class TestEmailSend(generics.GenericAPIView):
    def get(self,request, *args, **kwargs):

        email_obj = EmailMessage('email/index.tpl', {'name': 'Erfan'}, 'erfan6235@gmail.com',to=['erfanr926@gmail.com'])

        EmailThread(email_obj).start()

        return Response("email sent")