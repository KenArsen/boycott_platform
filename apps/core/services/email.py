import logging
from typing import List, Optional

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
