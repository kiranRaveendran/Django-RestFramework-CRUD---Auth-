from django.urls import path, include
from . views import *
urlpatterns = [
    path('', home),
    path('data_Manipulation/', data_Manipulation, name='data_Manipulation')
]
