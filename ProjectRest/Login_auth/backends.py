
from django.contrib.auth.backends import ModelBackend
from .models import PersonUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = PersonUser.objects.get(email=username)
        except PersonUser.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
