from django.contrib import admin
from .models import Student, Standard, StudentInfo
# Register your models here.
admin.site.register(Student)
admin.site.register(Standard)
admin.site.register(StudentInfo)
