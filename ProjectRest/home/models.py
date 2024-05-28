from django.db import models

# Create your models here.


class Standard(models.Model):
    student_STD = models.CharField(max_length=20)

    def __str__(self):
        return self.student_STD


class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    father_name = models.CharField(max_length=100)
    std = models.ForeignKey(Standard, null=True,
                            blank=True, on_delete=models.CASCADE, related_name='members', default=None)

    def __str__(self):
        return self.name


class StudentInfo(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    phone = models.CharField(max_length=20)
    distric = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name
