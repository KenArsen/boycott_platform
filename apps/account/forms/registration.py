from django import forms
from django.utils.translation import gettext_lazy as _

from apps.account.models import User


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label=_("Confirm Password"))

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "password", "confirm_password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("User with this email already exists."))
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(_("Passwords do not match."))

        return cleaned_data


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label=_("Confirmation code"),
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Enter 6-digit code"),
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
            }
        ),
    )

    def clean_code(self):
        code = self.cleaned_data["code"]
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError(_("Enter a valid 6-digit numeric code."))
        return code
