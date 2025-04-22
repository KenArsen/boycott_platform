from django import forms
from django.utils.translation import gettext_lazy as _


class ProductImageUploadForm(forms.Form):
    """Форма для загрузки изображения продукта"""

    image = forms.ImageField(
        label=_("Upload product image"),
        help_text=_("Upload an image of the product to get information about it"),
        widget=forms.FileInput(attrs={"accept": "image/*"}),
    )
