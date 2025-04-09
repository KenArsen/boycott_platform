import random
import string
import uuid
from datetime import timedelta

from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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


class Invitation(models.Model):
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_("Invitation Code"),
    )
    is_used = models.BooleanField(default=False, verbose_name=_("Is Used"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    expires_at = models.DateTimeField(
        default=get_default_expiration,
        verbose_name=_("Expires At"),
        help_text=_("Date and time when the invitation expires"),
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        verbose_name=_("Group"),
        help_text=_("Group assigned to the user upon registration"),
    )
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Registered User"),
        related_name="invitation",
    )

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.group.name})"

    def get_invitation_url(self):
        return reverse("account:registration-with-invite", kwargs={"code": self.code})

    def is_expired(self):
        expired = timezone.now() > self.expires_at
        return expired

    def is_valid(self):
        valid = not self.is_used and not self.is_expired()
        return valid

    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=["is_used"])
