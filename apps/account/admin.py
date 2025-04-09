import uuid

from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.account.forms.registration import InvitationForm
from apps.account.models import Invitation, User
from apps.core.services.email import EmailService

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


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "group_display",
        "code_short",
        "is_used",
        "created_at_short",
        "user_link",
    )
    list_filter = ("is_used", "group")
    search_fields = ("email",)
    form = InvitationForm
    actions = ["resend_invitation"]

    # Кастомные методы для отображения
    def code_short(self, obj):
        """Короткий UUID для списка"""
        return str(obj.code)[:8] + "..."

    code_short.short_description = _("Code")

    def created_at_short(self, obj):
        """Короткая дата создания"""
        return obj.created_at.strftime("%Y-%m-%d %H:%M")

    created_at_short.short_description = _("Created at")

    def user_link(self, obj):
        """Ссылка на зарегистрированного пользователя"""
        if obj.user:
            url = reverse("admin:account_user_change", args=[obj.user.pk])
            return mark_safe(f'<a href="{url}">{obj.user.email}</a>')
        return "-"

    user_link.short_description = _("Registered User")

    def group_display(self, obj):
        """Отображение группы"""
        return obj.group.name

    group_display.short_description = _("Group")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.code = uuid.uuid4()
            super().save_model(request, obj, form, change)
            EmailService.send_invitation_email(obj)
        else:
            super().save_model(request, obj, form, change)

    def resend_invitation(self, request, queryset):
        for invitation in queryset.filter(is_used=False):
            EmailService.send_invitation_email(invitation)
        self.message_user(request, _(f"Invitations resent to {queryset.count()} users."))

    resend_invitation.short_description = _("Resend selected invitations")

    # Ограничение прав
    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_role("Moderator")

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
