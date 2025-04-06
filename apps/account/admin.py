from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from apps.account.models import User

# Отменяем стандартную регистрацию
admin.site.unregister(Group)


# Переопределяем стандартный GroupAdmin
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "phone_number")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "groups"),
            },
        ),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "groups_display",
        "is_email_verified",
        "is_staff",
        "is_active",
        "created_at_short",
    )
    list_display_links = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "groups")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "last_login")

    # Кастомные методы
    def created_at_short(self, obj):
        """Короткая дата создания"""
        return obj.created_at.strftime("%Y-%m-%d %H:%M") if obj.created_at else "-"

    created_at_short.short_description = _("Created at")

    def groups_display(self, obj):
        """Отображение групп пользователя"""
        return ", ".join(group.name for group in obj.groups.all()) or "-"

    groups_display.short_description = _("Groups")

    # Ограничение прав
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_role("Moderator")

    def get_queryset(self, request):
        """Модераторы видят только обычных пользователей"""
        qs = super().get_queryset(request)
        if request.user.has_role("Moderator") and not request.user.is_superuser:
            return qs.exclude(groups__name="Admin")
        return qs
