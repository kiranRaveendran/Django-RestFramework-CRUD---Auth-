from rest_framework import serializers
from .models import *
import re
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

# Set Password: The set_password() method is called on the user object to
# set the password. This is a security measure provided by Django to properly hash and store passwords securely.


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']


class STDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = ['student_STD']


class StudentSerializer(serializers.ModelSerializer):

    std = STDSerializer()
    std_info = serializers.SerializerMethodField()

    class Meta:
        model = Student
        # fields = ['name', 'age']
        fields = '__all__'
        depth = 1  # to show all fiels in this row
        # exclude =

    def get_std_info(self, obj):
        return 'extra field'

    def validate(self, data):
        # spl_chars = '[!@#$%^&*(),.?":{}|<>]'
        pattern = r'[!@#$%^&*(),.?":{}|<>]'
        if data['name']:
            for item in data['name']:
                if item. isdigit():
                    raise serializers.ValidationError(
                        {'error': 'name can not be numeric'})
        # if any(ch in spl_chars for ch in data['name']):
        #     raise serializers.ValidationError(
        #         'Name should not have special characters')
        if re.search(pattern, data):
            raise serializers.ValidationError(
                'Name should not have special characters')

        if data['father_name'][0].islower():
            raise serializers.ValidationError(
                'Name should be start with capital letter')


class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = '__all__'
        depth = 1
