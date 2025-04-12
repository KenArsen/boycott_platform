import logging
import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.product.models import Product

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    """
    Удаляет изображение продукта при удалении продукта.
    """
    image_path = instance.image.path if instance.image else None
    if image_path and os.path.isfile(image_path):
        try:
            os.remove(image_path)
            logger.info(f"Изображение удалено: {image_path}")
        except Exception as e:
            logger.error(f"Ошибка при удалении изображения {image_path}: {e}")
