import random
import string
from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.account.models import User


def get_default_expiration():
    return timezone.now() + timedelta(hours=24)


class EmailVerificationCode(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="verification_code")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_expiration)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification code for {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def generate_code(cls):
        """Generate a random 6-digit code"""
        return "".join(random.choices(string.digits, k=6))

    @classmethod
    def create_verification_code(cls, user: User):
        """Create or update verification code for a user"""
        # Set expiration time (24 hours from now)
        expires_at = timezone.now() + timedelta(hours=24)

        # Check if user already has a verification code
        try:
            verification = cls.objects.get(user=user)
            verification.code = cls.generate_code()
            verification.expires_at = expires_at
            verification.is_verified = False
            verification.save()
        except cls.DoesNotExist:
            verification = cls.objects.create(user=user, code=cls.generate_code(), expires_at=expires_at)

        return verification
