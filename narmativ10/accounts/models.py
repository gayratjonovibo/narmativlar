import random
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

def generate_code():
    return random.randint(100000, 999999)

def exp_time_now():
    return timezone.now() + timedelta(minutes=2)

class PasswordResetCode(models.Model):
    code = models.PositiveIntegerField(default=generate_code)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_codes')
    expired_date = models.DateTimeField(default=exp_time_now)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expired_date

    def __str__(self):
        return f"{self.user.username} - {self.code}"