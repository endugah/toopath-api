from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from TooPath3.constants import DEFAULT_ERROR_MESSAGES
from TooPath3.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):
        if self.partial is True:
            if 'pk' in data or 'id' in data or 'email' in data or 'username' in data:
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['invalid_patch'])
            if bool(data) is False or len(self.initial_data) != len(data):
                raise serializers.ValidationError(DEFAULT_ERROR_MESSAGES['patch_device_fields_required'])
        if 'password' in data:
            data['password'] = make_password(data['password'])
        return data


# Custom User Serializer for GET methods
class PublicCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class GoogleLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    google_token = serializers.CharField(required=True)
    name = serializers.CharField()
