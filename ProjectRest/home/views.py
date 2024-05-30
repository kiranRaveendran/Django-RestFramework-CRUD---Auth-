from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
# as it is class based view we should specify with : as_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
# from .authentication import ExpiringTokenAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
# from rest_framework.paginator import PageNumberPagination
# from rest_framework import viewsets
# Create your views here.


class RegisterUser(APIView):  # class based view
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'error': serializer.errors, 'message': 'some error occurs'})
        serializer.save()

        # user = User.objects.get(username=serializer.data['username'])
        # Token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 200, 'payload': serializer.data,  'message': 'Your registeration is done'})


class LoginAPI(APIView):
    # making this permission_classes value as empty or AllowAny to make everyone can access this class url.
    permission_classes = [AllowAny]

    # def generate_access_token(self, user):
    #     # Define the desired expiration time
    #     access_token_lifetime = timedelta(seconds=30)  # Example: 30 minutes
    #     # Create an access token instance with the desired expiration time
    #     access_token = AccessToken.for_user(user)
    #     access_token.set_exp(access_token_lifetime)
    #     return access_token

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors, })

        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({"message": "invalid credentials"})

        try:
            # access_token = self.generate_access_token(user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
        except TokenError:
            return Response({"message": "Access token generation failed. Please try again."}, status=500)
        # access_token = self.generate_access_token(user)
        return Response({'message': 'Login successfull', 'token': str(access_token)})

# how to access cash ?-----------------------------------------------------------
# default time duration for token expiry
# access token and refresh token this can used to only create new access token.


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            # Blacklist the refresh token to invalidate it
            user_token = request.user.auth_token
            if user_token:
                user_token.delete()
            else:
                return Response({"message": "No refresh token provided."}, status=400)
            return Response({"message": "Logout successful."}, status=200)
        except Exception as e:
            return Response({"message": str(e)}, status=400)


class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):  # Generic view
    # ListAPIView : get method
    # CreateAPIView :post method
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ClassStudent(APIView):  # class based view
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # here we do not want to explicitly wirte the condition to check which method is this or not like: if request.method == 'GET':

    def get(self, request):
        objstudent = Student.objects.filter()
        serializer = StudentSerializer(
            objstudent, many=True)  # many=True: to get more than one data
        return Response(serializer.data)

    def post(self, request):
        return Response('This is post method from API')


class StudentInfoCRUD1(generics.ListAPIView, generics.CreateAPIView):  # Generic view
    # ListAPIView : get method
    # CreateAPIView :post method
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer


class StudentInfoCRUD2(generics.UpdateAPIView, generics.DestroyAPIView):  # Generic view
    # UpdateAPIView : put or patch method
    # DestroyAPIView :delete method
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer
    lookup_field = 'id'


@ api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])  # Function based view
def home(request):
    if request.method == 'POST':
        return Response('POST request responds redmo')
    if request.method == 'GET':
        return Response('GET request responds redmo')
    if request.method == 'PUT':
        return Response('PUT request responds redmo')
    if request.method == 'PATCH':
        return Response('PATCH request responds redmo')
    if request.method == 'DELETE':
        return Response('DELETE request responds redmo')


@ api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])  # Function based view
def data_Manipulation(request):
    if request.method == 'GET':
        objstudent = Student.objects.filter(std__isnull=False)
        serializer = StudentSerializer(
            objstudent, many=True)  # many=True: to get more than one data
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = StudentSerializer(data=data)
        if request.data['age'] < 18:
            return Response({'Age should be 18 or greater'})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        obj = Student.objects.get(id=data['id'])
        serializer = StudentSerializer(obj, data=data, partial=False)
        if request.data['age'] < 18:
            return Response({'Age should be 18 or greater'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data
        obj = Student.objects.get(id=data['id'])
        serializer = StudentSerializer(obj, data=data, partial=True)
        if request.data['age'] < 18:
            return Response({'Age should be 18 or greater'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data = request.data
        obj = Student.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Student record is removed'})
