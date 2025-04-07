import logging
from typing import List, Optional

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task
def send_email_task(
    subject: str,
    to_emails: List[str],
    plain_message: str,
    from_email: Optional[str] = None,
    html_template: Optional[str] = None,
    template_context: Optional[dict] = None,
) -> bool:
    """Асинхронная задача для отправки email."""
    try:
        from_email = from_email or settings.EMAIL_HOST_USER
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=to_emails,
        )
        if html_template and template_context is not None:
            html_message = render_to_string(html_template, template_context)
            email.attach_alternative(html_message, "text/html")

        email.send(fail_silently=False)
        logger.info(f"Email успешно отправлен на {to_emails}")
        return True
    except FileNotFoundError as e:
        logger.error(f"Шаблон '{html_template}' не найден: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при отправке email на {to_emails}: {str(e)}", exc_info=True)
        raise
