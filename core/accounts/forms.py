from django import forms
from accounts.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):
    phone = forms.CharField(label="تلفن همراه", required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("رمز عبور و تایید آن یکسان نیستند")
        return cleaned_data

class CustomLoginForm(forms.Form):
    email = forms.CharField(label="ایمیل")
    password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور")
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(username=email, password=password) 
            if not user:
                raise forms.ValidationError("ایمیل یا رمز عبور نادرست است.")
            self.user = user
        return self.cleaned_data

    def get_user(self):
        return self.user