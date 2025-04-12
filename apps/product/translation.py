from modeltranslation.translator import TranslationOptions, register

from apps.product.models import Category, Product, Reason


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Reason)
class ReasonTranslationOptions(TranslationOptions):
    fields = ("title", "description")
