from django import forms

from apps.account.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number"]
        widgets = {"email": forms.TextInput(attrs={"readonly": "readonly"})}
