import logging
from typing import List, Optional

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from apps.account.models import Invitation
from apps.core.tasks import send_email_task

logger = logging.getLogger(__name__)


class EmailService:
    """Сервис для отправки email-сообщений."""

    @staticmethod
    def send_email(
        subject: str,
        to_emails: List[str],
        plain_message: str,
        from_email: Optional[str] = None,
        html_template: Optional[str] = None,
        template_context: Optional[dict] = None,
    ) -> bool:
        """
        Отправляет email-сообщение асинхронно через Celery.

        Returns:
            bool: Успешно ли задача поставлена в очередь.
        """
        try:
            # Запускаем задачу асинхронно
            result = send_email_task.delay(
                subject=subject,
                to_emails=to_emails,
                plain_message=plain_message,
                from_email=from_email,
                html_template=html_template,
                template_context=template_context,
            )
            logger.info(f"Задача отправки email на {to_emails} поставлена в очередь: {result.id}")
            return True  # Возвращаем True, если задача успешно поставлена
        except Exception as e:
            logger.error(f"Ошибка при постановке задачи отправки email на {to_emails}: {str(e)}")
            raise Exception(f"Ошибка при постановке задачи отправки email: {str(e)}")

    @staticmethod
    def send_invitation_email(invitation: Invitation) -> bool:
        """Отправляет письмо-приглашение на регистрацию."""
        template_context = {
            "email": invitation.email,
            "code": invitation.code,
            "group_name": invitation.group.name,
            "invitation_url": f"{settings.DOMAIN}{invitation.get_invitation_url()}",
        }
        plain_message = _(
            f"""Вы были приглашены зарегистрироваться на платформе Boycott Products Platform.
            Группа: {template_context['group_name']}
            Ссылка на регистрацию: {template_context['invitation_url']}
            Если вы не запрашивали это, просто проигнорируйте это письмо."""
        )

        return EmailService.send_email(
            subject=_("Вы приглашены на регистрацию"),
            to_emails=[invitation.email],
            plain_message=plain_message,
            html_template="register/invitation_send.html",
            template_context=template_context,
        )
