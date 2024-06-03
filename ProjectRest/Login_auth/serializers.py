from rest_framework import serializers
from .models import User_class


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_class
        # Customize fields as needed
        fields = ('id', 'email', 'username', 'phone_number')

class OTPSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
