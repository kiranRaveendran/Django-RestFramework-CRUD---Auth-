
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
# as it is class based view we should specify with : as_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
# from rest_framework import viewsets
# Create your views here.


class RegisterUser(APIView):  # class based view
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'error': serializer.errors, 'message': 'some error occurs'})
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        Token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 200, 'payload': serializer.data, 'token': str(Token_obj), 'message': 'Your registeration is done'})


class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):  # Generic view
    # ListAPIView : get method
    # CreateAPIView :post method
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ClassStudent(APIView):  # class based view
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer


class StudentInfoCRUD2(generics.UpdateAPIView, generics.DestroyAPIView):  # Generic view
    # UpdateAPIView : put or patch method
    # DestroyAPIView :delete method
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


# /////////////////////////////////View set


class StudentViewSet(viewsets.ViewSet):

    # A simple ViewSet for listing or retrieving .
    def list(self, request):
        queryset = Student.objects.all()
        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Student.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = StudentSerializer(user)
        return Response(serializer.data)
