import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from typing import List, Optional

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
    ):
        """
        Отправляет email-сообщение.

        Args:
            subject: Тема письма.
            to_emails: Список адресов получателей.
            plain_message: Текстовое сообщение (обязательно).
            from_email: Адрес отправителя (по умолчанию из настроек).
            html_template: Путь к HTML-шаблону (опционально).
            template_context: Контекст для рендеринга шаблона (опционально).

        Returns:
            bool: Успешно ли отправлено письмо.
        """
        try:
            # Устанавливаем отправителя по умолчанию из настроек, если не указан
            from_email = from_email or settings.EMAIL_HOST_USER

            # Создаём объект письма
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=from_email,
                to=to_emails,
            )

            # Если передан HTML-шаблон, рендерим и прикрепляем его
            if html_template and template_context is not None:
                html_message = render_to_string(html_template, template_context)
                email.attach_alternative(html_message, "text/html")

            # Отправляем письмо
            email.send(fail_silently=False)
            logger.info(f"Email успешно отправлен на {to_emails}")
        except FileNotFoundError as e:
            logger.error(f"Шаблон '{html_template}' не найден: {str(e)}")
            raise FileNotFoundError(f"Шаблон '{html_template}' не найден: {str(e)}")

        except Exception as e:
            logger.error(f"Ошибка при отправке email на {to_emails}: {str(e)}", exc_info=True)
            raise Exception(f"Ошибка при отправке email на {to_emails}: {str(e)}")