from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        بررسی می‌کند که password و confirm_password یکسان باشند.
        """
        confirm_password = data.pop('confirm_password', None)  # حذف قبل از ذخیره
        if data['password'] != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
    

