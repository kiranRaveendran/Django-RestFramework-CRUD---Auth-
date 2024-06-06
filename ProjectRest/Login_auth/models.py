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
