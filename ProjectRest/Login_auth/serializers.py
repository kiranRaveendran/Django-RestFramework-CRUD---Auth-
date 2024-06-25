from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import PersonUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from .backends import *
from .utils import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site


class PersonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonUser
        fields = ['id', 'email', 'otp', 'groups', 'user_permissions']


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = PersonUser
        fields = ('email', 'password')

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')

        validated_data.pop('email')
        validated_data.pop('password')

        user = PersonUser.objects.create_user(
            email=email, password=password, **validated_data)
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Use the custom authentication backend
        user = authenticate(username=email, password=password)
        print(f'Authenticating user: {email} and password {password}')

        if not user:
            print('Invalid credentials')
            raise serializers.ValidationError('Invalid credentials')

        if not user.is_active:
            print('User account is not active')
            raise serializers.ValidationError('User account is not active')

        data['user'] = user
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = PersonUser.objects.get(pk=uid)
            if not PasswordResetTokenGenerator().check_token(user, data['token']):
                raise serializers.ValidationError('Invalid token or user ID')
        except (TypeError, ValueError, OverflowError, PersonUser.DoesNotExist):
            raise serializers.ValidationError('Invalid token or user ID')

        return data

    def save(self):
        uid = force_str(urlsafe_base64_decode(self.validated_data['uidb64']))
        user = PersonUser.objects.get(pk=uid)
        user.set_password(self.validated_data['password'])
        user.save()
