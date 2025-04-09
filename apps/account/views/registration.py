import logging
from uuid import UUID

from django.contrib import messages
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.account.forms.registration import EmailVerificationForm, RegistrationForm
from apps.account.models import EmailVerificationCode, Invitation, User
from apps.account.services.registration import RegistrationService

logger = logging.getLogger(__name__)


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                registration_service = RegistrationService(
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    phone_number=form.cleaned_data["phone_number"],
                )
                user, verification_code = registration_service.register()
                request.session["user"] = str(user.pk)  # Сохраняем UUID как строку
                logger.info(f"Регистрация успешна для {user.email}, отправлен код верификации")
                messages.success(request, "Регистрация прошла успешно! Проверьте ваш email для подтверждения.")
                return redirect("account:verify-email")
            except ValidationError as e:
                logger.warning(f"Ошибка валидации при регистрации: {str(e)}")
                messages.error(request, str(e))
            except Exception as e:
                logger.error(f"Ошибка при регистрации: {str(e)}")
                messages.error(request, f"Ошибка при регистрации: {str(e)}")
        else:
            logger.debug(f"Форма регистрации невалидна: {form.errors}")
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
        return render(request, "register/registration.html", {"form": form})
    else:
        form = RegistrationForm()
        return render(request, "register/registration.html", {"form": form})


def verify(request):
    # Проверяем, есть ли user в сессии
    user_id = request.session.get("user")
    if not user_id:
        logger.warning("Попытка верификации без user_id в сессии")
        messages.error(request, "Сессия недействительна. Пожалуйста, зарегистрируйтесь заново.")
        return redirect("account:registration")

    try:
        user = User.objects.get(pk=UUID(user_id))
    except (User.DoesNotExist, ValueError):
        logger.error(f"Пользователь с ID {user_id} не найден или ID некорректен")
        messages.error(request, "Пользователь не найден. Пожалуйста, зарегистрируйтесь заново.")
        return redirect("account:registration")

    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"].strip()
            try:
                verification = EmailVerificationCode.objects.get(user=user, code=code)
                if verification.is_expired():
                    logger.warning(f"Код {code} для {user.email} истёк")
                    messages.error(request, "Срок действия кода истёк.")
                else:
                    user.is_email_verified = True  # Приводим к единообразию с RegistrationService
                    user.save()
                    verification.delete()
                    logger.info(f"Email {user.email} успешно подтверждён")
                    messages.success(request, "Email успешно подтверждён!")
                    del request.session["user"]  # Очищаем сессию
                    return redirect("home")
            except EmailVerificationCode.DoesNotExist:
                logger.debug(f"Неверный код {code} для {user.email}")
                messages.error(request, "Неверный код.")
        else:
            logger.debug(f"Форма верификации невалидна: {form.errors}")
            messages.error(request, "Пожалуйста, введите корректный код.")
    else:
        form = EmailVerificationForm()

    return render(request, "register/verify_email.html", {"form": form})


def register_by_invitation_view(request, code):
    # Проверка приглашения
    try:
        invitation = Invitation.objects.get(
            code=code,
            is_used=False,
            expires_at__gt=timezone.now(),
        )
    except Invitation.DoesNotExist:
        raise Http404(_("Приглашение не найдено, уже использовано или истекло."))

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = invitation.email
            user.is_email_verified = True
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Добавление в группу и установка прав
            user.groups.add(invitation.group)
            if invitation.group.name == "Moderator":
                user.is_staff = True
            elif invitation.group.name == "Admin":
                user.is_staff = True
                user.is_superuser = True
            user.save()

            # Обновление приглашения
            invitation.user = user
            invitation.is_used = True
            invitation.save()

            login(request, user)
            return redirect("admin:index")
        else:
            logger.debug(f"Форма регистрации невалидна: {form.errors}")
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = RegistrationForm(initial={"email": invitation.email})

    context = {
        "form": form,
        "invitation": invitation,
    }
    return render(request, "register/register_with_invitation.html", context)
