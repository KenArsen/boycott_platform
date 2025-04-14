from django import forms

class AskForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
