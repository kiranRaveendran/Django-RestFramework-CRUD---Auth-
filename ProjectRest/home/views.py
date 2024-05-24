from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.


@api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
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


@api_view(['POST', 'GET', 'PUT', 'PATCH', 'DELETE'])
def data_Manipulation(request):
    if request.method == 'GET':
        objstudent = Student.objects.all()
        serializer = StudentSerializer(
            objstudent, many=True)  # many=True: to get more than one data
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        obj = Student.objects.get(id=data['id'])
        serializer = StudentSerializer(obj, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data
        obj = Student.objects.get(id=data['id'])
        serializer = StudentSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    else:
        data = request.data
        obj = Student.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': 'Student record is removed'})
