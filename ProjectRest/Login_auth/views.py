from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import User_class
from .serializers import UserSerializer, OTPSerializer


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'Please provide email address.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User_class.objects.get(email=email)
            user.generate_otp()  # Generate and store OTP
            # Send OTP via email (replace with your logic)
            send_mail(
                'Email OTP Verification',
                f'Your OTP code is {user.otp}',
                'youremail@example.com',  # Replace with your email
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email.'})
        except User_class.DoesNotExist:
            return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        if not email or not code:
            return Response({'message': 'Please provide both email and OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User_class.objects.get(email=email)
            if user.verify_otp(code):
                # Login logic (e.g., generate JWT token)
                return Response({'message': 'OTP verified successfully.'})
            else:
                return Response({'message': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
        except User_class.DoesNotExist:
            return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'message': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if user:
            # Login logic (e.g., generate JWT token)
            return Response({'message': 'Login successful.'})
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
