from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # اگه ایمیل تأیید شده باشه، مستقیم لاگین کن
        if sociallogin.user.email:
            return True
        # در غیر این صورت، کاربر باید اطلاعات وارد کنه
        return False

    def pre_social_login(self, request, sociallogin):
        # اگه کاربر از قبل تو دیتابیس باشه، مستقیم لاگین کن
        if sociallogin.is_existing:
            return

        # اگه ایمیل وجود داره ولی هنوز ثبت‌نام نکرده، اکانتش رو بساز و لاگین کن
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
                pass  # ادامه بده، ثبت‌نام خودکار انجام بشه
