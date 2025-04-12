from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.product.models import Category, Product, Reason, Review


# Админка для Category
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}  # Автозаполнение slug из name
    ordering = ("name",)

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {"all": ("modeltranslation/css/tabbed_translation_fields.css",)}


# Админка для Reason
@admin.register(Reason)
class ReasonAdmin(TranslationAdmin):
    list_display = ("title", "description_short")
    search_fields = ("title", "description")
    ordering = ("title",)

    def description_short(self, obj):
        """Укорачивает описание для отображения в списке"""
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description

    description_short.short_description = _("Description")

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {"all": ("modeltranslation/css/tabbed_translation_fields.css",)}


# Форма для выбора альтернативного продукта
class AlternativeProductForm(forms.Form):
    target_product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label=_("Alternative product"),
        help_text=_("Selected products will be linked as alternatives to this product."),
    )


# Админка для Product
@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    def image_preview(self, obj):
        """Превью изображения товара"""
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-width: 50px; max-height: 50px; border-radius: 5px;" />'
            )
        return _("No image")

    image_preview.short_description = _("Image Preview")

    # Поля и их группировка
    fieldsets = (
        (
            None,
            {"fields": ("name", "category", "description", "image", "image_preview")},
        ),
        (_("Boycott Information"), {"fields": ("is_boycotted", "boycott_reason")}),
        (
            _("Additional Info"),
            {"fields": ("is_kyrgyz_product", "alternative_products")},
        ),
        (_("Statistics"), {"fields": ("query_count", "get_rating")}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = (
        "query_count",
        "created_at",
        "updated_at",
        "image_preview",
        "get_rating",
    )
    list_display = (
        "name",
        "category",
        "is_boycotted",
        "query_count",
        "get_rating_display",
        "is_kyrgyz_product",
        "image_preview",
    )
    list_filter = ("category", "is_boycotted", "is_kyrgyz_product")
    search_fields = ("name", "description", "category__name")
    ordering = ("-query_count",)
    filter_horizontal = ("alternative_products",)  # Удобный интерфейс для ManyToMany

    # Кастомные действия
    actions = ["mark_as_boycotted", "mark_as_not_boycotted", "add_alternative_products"]

    # Ограничение прав
    def has_add_permission(self, request):
        return request.user.is_superuser  # Только суперпользователи могут добавлять

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Только суперпользователи могут удалять

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_moderator()  # Модераторы могут редактировать

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_moderator()  # Модераторы могут просматривать

    def mark_as_boycotted(self, request, queryset):
        """Массово помечает товары как бойкотируемые"""
        updated = queryset.update(is_boycotted=True)
        self.message_user(request, _(f"Marked {updated} products as boycotted."))

    mark_as_boycotted.short_description = _("Mark selected products as boycotted")

    def mark_as_not_boycotted(self, request, queryset):
        """Массово снимает отметку бойкота"""
        updated = queryset.update(is_boycotted=False)
        self.message_user(request, _(f"Removed boycott mark from {updated} products."))

    mark_as_not_boycotted.short_description = _("Remove boycott mark from selected products")

    def add_alternative_products(self, request, queryset):
        """Массово добавляет альтернативный товар"""
        if "apply" in request.POST:
            form = AlternativeProductForm(request.POST)
            if form.is_valid():
                target_product = form.cleaned_data["target_product"]
                if target_product.is_boycotted:
                    self.message_user(
                        request,
                        _("A boycotted product cannot be an alternative!"),
                        level="error",
                    )
                    return
                for product in queryset:
                    if product != target_product:
                        product.alternative_products.add(target_product)
                self.message_user(request, _(f"Alternatives added to {queryset.count()} products."))
                return
        form = AlternativeProductForm()
        return {
            "form": form,
            "queryset": queryset,
            "title": _("Add alternative product"),
            "action": "add_alternative_products",
        }

    add_alternative_products.short_description = _("Add selected products as alternatives")

    def get_rating_display(self, obj):
        """Отображение рейтинга в списке"""
        return obj.get_rating()

    get_rating_display.short_description = _("Rating")

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {"all": ("modeltranslation/css/tabbed_translation_fields.css",)}


# Админка для Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at_short")
    list_filter = ("rating", "created_at", "product__category")
    search_fields = ("product__name", "user__email", "comment")
    ordering = ("-created_at",)

    def created_at_short(self, obj):
        """Короткая дата создания"""
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    created_at_short.short_description = _("Created at")
