from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from accounts.api.v1.serializer import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordApiSerializer,
    ProfileSerializer,
    ActivationResendEmailSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer,
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
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
import jwt
from django.conf import settings

User = get_user_model()


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        email = serializer.validated_data["email"]
        user = get_object_or_404(User, email=email)
        token = self.get_tokens_for_user(user)
        email_body = render_to_string(
            "email/activation_email.tpl", {"token": token}
        )
        email_obj = EmailMessage(
            "Registration Confirmation", email_body, to=[email]
        )
        EmailThread(email_obj).start()

        data = {
            "email": email,
            "detail": "User registered successfully",
            "Activation": "Check your email for the activation link",
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "Token not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


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
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )

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
    def get(self, request, *args, **kwargs):
        """This is a create token and send it to the email address of
        the user."""
        self.email = "ali@ali.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        email_body = render_to_string("email/index.tpl", {"token": token})
        email_obj = EmailMessage(
            "email/index.tpl",
            email_body,
            "erfan6235@gmail.com",
            to=[self.email],
        )
        EmailThread(email_obj).start()
        return Response("email sent")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationConfirmEmailView(generics.GenericAPIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")
            user = User.objects.get(id=user_id)
            if user.is_verified:
                return Response(
                    {"detail": "Account already activated"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_verified = True
            user.save()
            return Response(
                {"detail": "Account activated successfully"},
                status=status.HTTP_200_OK,
            )

        except jwt.ExpiredSignatureError:
            return Response(
                "Activation link expired", status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.DecodeError:
            return Response(
                "Invalid token", status=status.HTTP_400_BAD_REQUEST
            )


class ActivationResendEmailView(generics.GenericAPIView):
    serializer_class = ActivationResendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_body = render_to_string(
            "email/activation_email.tpl", {"token": token}
        )
        email_obj = EmailMessage(
            "Registration Confirmation", email_body, to=[user_obj.email]
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "Activation email resent successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data["email"])

        token = RefreshToken.for_user(user).access_token
        email_body = render_to_string(
            "email/reset_password_email.tpl",
            {
                "token": str(token),
            },
        )
        email = EmailMessage(
            "Reset Your Password", email_body, to=[user.email]
        )
        EmailThread(email).start()

        return Response(
            {"detail": "Reset password link is send to your email."},
            status=status.HTTP_200_OK,
        )


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, token):
        try:
            decode = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = User.objects.get(id=decode["user_id"])
        except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            User.DoesNotExist,
        ):
            return Response(
                {"error": "token is invalid or expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(
            {"detail": "password is changed successfully."},
            status=status.HTTP_200_OK,
        )
