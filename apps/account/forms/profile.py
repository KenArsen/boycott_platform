from django import forms
from django.contrib.auth.forms import UserChangeForm

from apps.account.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number"]
        widgets = {"email": forms.TextInput(attrs={"readonly": "readonly"})}


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
