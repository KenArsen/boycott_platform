from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import CoreModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, group_names=None, **extra_fields):
        if group_names is None:
            group_names = ["User"]
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        for name in group_names:
            group, _ = Group.objects.get_or_create(name=name)
            user.groups.add(group)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email, password, ["Admin"], **extra_fields)
        return user


class User(CoreModel, AbstractUser):
    username = None
    date_joined = None
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    first_name = models.CharField(max_length=255, blank=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, blank=True, verbose_name=_("Last Name"))
    phone_number = models.CharField(max_length=255, blank=True, verbose_name=_("Phone Number"))
    is_email_verified = models.BooleanField(default=False, verbose_name=_("Email Verified"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_role(self, role_name):
        has_role = self.groups.filter(name=role_name).exists()
        return has_role
