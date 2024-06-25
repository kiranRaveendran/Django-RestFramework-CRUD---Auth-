from django.contrib.auth.models import UserManager
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
from django.contrib.auth.models import User


class OTP:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional: Set an expiry time for OTP
    valid_until = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"OTP for {self.user.username}"


# Create your models here.


class PersonUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.pop('email', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class PersonUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = PersonUserManager()

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, email, password=None, **extra_fields):
        email = cls.normalize_email(email)
        user = cls(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_query_name="%(app_label)s_%(class)s",
        related_name="+",
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_query_name="%(app_label)s_%(class)s",
        related_name="+",
        help_text=_('Specific permissions for this user.'),
    )
