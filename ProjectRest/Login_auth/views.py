import smtplib
from email.mime.text import MIMEText
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializers import UserSerializer
from django.conf import settings
from django.contrib.auth.models import User
import secrets


# class UserRegistrationView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User created successfully.'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_otp(email, otp):
    message = MIMEText(f"Your OTP for registration is {otp}.", 'plain')
    message['Subject'] = 'User Registration OTP'
    # Replace with your sender email
    message['From'] = settings.EMAIL_HOST_USER
    message['To'] = email
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(message['From'], message['To'], message.as_string())


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            otp = secrets.token_urlsafe(6)
            print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk testss')

            user = User(**serializer.validated_data)  # Unpack validated data

            send_otp(user.email, otp)  # Send OTP to user's email

            return Response({
                'message': 'A verification OTP has been sent to your email.',
                'username': user.username,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RequestOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         if not email:
#             return Response({'message': 'Please provide email address.'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = UserSerializer.objects.get(email=email)
#             user.generate_otp()  # Generate and store OTP
#             # Send OTP via email (replace with your logic)
#             send_mail(
#                 'Email OTP Verification',
#                 f'Your OTP code is {user.otp}',
#                 'youremail@example.com',  # Replace with your email
#                 [user.email],
#                 fail_silently=False,
#             )
#             return Response({'message': 'OTP sent to your email.'})
#         except UserSerializer.DoesNotExist:
#             return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_REQUEST)


# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         code = request.data.get('code')
#         if not email or not code:
#             return Response({'message': 'Please provide both email and OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = UserSerializer.objects.get(email=email)
#             if user.verify_otp(code):
#                 # Login logic (e.g., generate JWT token)
#                 return Response({'message': 'OTP verified successfully.'})
#             else:
#                 return Response({'message': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)
#         except UserSerializer.DoesNotExist:
#             return Response({'message': 'Invalid email address.'}, status=status.HTTP_400_BAD_)


# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if not email or not password:
#             return Response({'message': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(email=email, password=password)
#         if user:
#             # Login logic (e.g., generate JWT token)
#             return Response({'message': 'Login successful.'})
#         return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
