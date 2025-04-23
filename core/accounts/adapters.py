from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        if sociallogin.user.email:
            return True
        return False

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return

        if sociallogin.account.provider == "google":
            user = sociallogin.user
            if not user.email:
                return

            from django.contrib.auth import get_user_model

            User = get_user_model()
            try:
                existing_user = User.objects.get(email=user.email)
                sociallogin.connect(request, existing_user)
                raise ImmediateHttpResponse(redirect("/"))
            except User.DoesNotExist:
                pass
