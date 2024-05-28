from django.urls import path, include
from . views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stud-viewset', StudentViewSet,
                basename='Student')
urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('StudentGeneric/', StudentGeneric.as_view(), name='StudentGeneric'),
    path('StudentInfoCRUD1/', StudentInfoCRUD1.as_view(), name='StudentInfoCRUD1'),
    path('StudentInfoCRUD2/<id>/', StudentInfoCRUD2.as_view(),
         name='StudentInfoCRUD2'),
    path('home', home),
    # path('data-Manipulation/', data_Manipulation, name='data_Manipulation'),
    path('class-student/', ClassStudent.as_view(), name='class-student'),
    path('RegisterUser/', RegisterUser.as_view(), name='RegisterUser')
]
