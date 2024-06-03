from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random  # To generate OTP

class User_class(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)  # Optional phone number
    otp = models.CharField(max_length=6, blank=True)  # Store OTP for verification
    otp_requested_at = models.DateTimeField(blank=True, null=True)  # Track OTP request time

    def generate_otp(self):
        self.otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
        self.otp_requested_at = timezone.now()
        self.save()

    def verify_otp(self, code):
        if self.otp == code and self.otp_requested_at and (timezone.now() - self.otp_requested_at) < timezone.timedelta(minutes=10):
            self.otp = ""  # Clear OTP after successful verification
            self.otp_requested_at = None
            self.save()
            return True
        return False
