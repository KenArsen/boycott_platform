from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.account.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number"]
        widgets = {"email": forms.TextInput(attrs={"readonly": "readonly"})}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserAdminChangeForm(UserChangeForm):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    class Meta:
        model = User
        fields = "__all__"
