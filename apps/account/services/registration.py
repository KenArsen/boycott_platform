import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from apps.account.models import EmailVerificationCode, User
from apps.core.services.email import EmailService

logger = logging.getLogger(__name__)


class RegistrationService:
    def __init__(
        self,
        email: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        phone_number: str = "",
        group_names: list = None,
        is_email_verified: bool = False,
    ):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.is_email_verified = is_email_verified
        self.group_names = group_names or ["User"]
        self.user = None
        self.verification_code = None

    def create_user(self):
        if User.objects.filter(email=self.email).exists():
            raise ValidationError(_("Пользователь с таким email уже существует"))
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            phone_number=self.phone_number,
            group_names=self.group_names,
            is_email_verified=False,
        )
        logger.info(f"Пользователь создан: {self.user.email}")

    def create_verification_code(self):
        self.verification_code = EmailVerificationCode.create_verification_code(self.user)
        logger.info(f"Код верификации сгенерирован для {self.user.email}")

    def send_verification_email(self):
        # Текстовая версия сообщения на русском
        plain_message_template = _(
            f"""Здравствуйте, {self.user.first_name}!\n\n
            Пожалуйста, подтвердите ваш email для платформы Boycott Products Platform.\n
            Ваш код верификации: {self.verification_code.code}\n
            Этот код действителен в течение 24 часов.\n\n
            Спасибо!"""
        )
        plain_message = plain_message_template % {
            "first_name": self.user.first_name or "Пользователь",
            "site_name": "Платформа бойкота продуктов",
            "code": self.verification_code.code,
            "expiry_hours": 24,
        }

        # Отправка письма
        success = EmailService.send_email(
            subject=_("Подтверждение email-адреса"),
            to_emails=[self.user.email],
            plain_message=plain_message,
            html_template="register/send_verify_email_code.html",
            template_context={
                "name": self.verification_code.user.get_full_name(),
                "code": self.verification_code.code,
                "site_name": "Платформа бойкота продуктов",
                "expiry_hours": 24,
            },
        )
        if success:
            logger.info(f"Письмо с верификацией отправлено на {self.user.email}")
        else:
            logger.error(f"Не удалось отправить письмо на {self.user.email}")
            raise Exception(_("Не удалось отправить письмо с верификацией"))

    def register(self):
        try:
            with transaction.atomic():
                self.create_user()
                self.create_verification_code()
                self.send_verification_email()
                return self.user, self.verification_code
        except Exception as e:
            logger.error(f"Ошибка регистрации для {self.email}: {str(e)}")
            raise
