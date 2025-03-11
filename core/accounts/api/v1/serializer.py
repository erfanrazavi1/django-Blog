from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        
        try:
            validators.validate_password(password=data.get('password')) 
            # This will raise a ValidationError if the password is invalid
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError({"password": list(e.messages)})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user
    

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data
    
    

class ChangePasswordApiSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError({"new_password": "Passwords do not match."})
        
        try:
            validators.validate_password(password=data.get('new_password')) 
            # This will raise a ValidationError if the password is invalid
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError({"new_password": list(e.messages)})
        return data