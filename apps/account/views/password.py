from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.urls import reverse_lazy

from apps.account.forms.authentication import CustomPasswordChangeForm


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "register/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("account:login")


class CustomPasswordResetView(PasswordResetView):
    template_name = "register/password_reset.html"
    email_template_name = "register/password_reset_email.html"
    success_url = reverse_lazy("account:login")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "register/password_reset_confirm.html"
    success_url = reverse_lazy("account:login")
