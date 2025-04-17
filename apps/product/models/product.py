from django.db import models
from django.db.models import Avg, F, Max, OuterRef, Subquery
from django.utils.translation import gettext_lazy as _

from apps.account.models import User
from apps.core.models import CoreModel


def product_image_upload_path(instance, filename):
    """Формирует путь для сохранения изображения в формате 'products/<category_slug>/<product_id>.jpg'"""
    extension = filename.split(".")[-1]  # Получаем расширение файла
    return f"products/logos/{instance.category.slug}/{instance.pk}.{extension}"


class Category(CoreModel):
    """Категория товаров (например, Напитки, Косметика)"""

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Category name"))
    slug = models.SlugField(unique=True, verbose_name=_("Category slug"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Reason(models.Model):
    """Причина бойкота (например, Эксплуатация детского труда, Экологический вред)"""

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Boycott reason")
        verbose_name_plural = _("Boycott reasons")

    def __str__(self):
        return self.title


class Product(CoreModel):
    """Основная модель товара"""

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Category"),
    )
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_boycotted = models.BooleanField(default=False, verbose_name=_("Is boycotted"))
    boycott_reason = models.ForeignKey(
        to=Reason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Boycott reason"),
    )
    query_count = models.IntegerField(default=0, verbose_name=_("Query count"))
    is_kyrgyz_product = models.BooleanField(default=False, verbose_name=_("Is kyrgyz product"))
    image = models.ImageField(
        upload_to=product_image_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )
    alternative_products = models.ManyToManyField(to="self", blank=True, verbose_name=_("Alternative products"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    def get_rating(self):
        """
        Рассчитывает рейтинг от 1 до 5 на основе query_count и отзывов, с использованием аннотаций.
        """
        # Аннотируем максимальное количество запросов по категории и средний рейтинг по отзывам
        product = (
            Product.objects.filter(pk=self.pk)
            .annotate(max_queries=Max("category__products__query_count"), avg_rating=Avg("reviews__rating"))
            .first()
        )

        # Нормализуем на основе максимума
        normalized_query_count = (self.query_count / product.max_queries) * 4 if product.max_queries else 0

        # Средний рейтинг от отзывов (или 3, если отзывов нет)
        average_review_rating = product.avg_rating or 3

        # Усредняем запросы и отзывы
        weighted_rating = (normalized_query_count + average_review_rating) / 2

        # Ограничиваем рейтинг от 1 до 5 и возвращаем
        return round(min(5, max(1, weighted_rating)), 2)

    @classmethod
    def get_sorted_products(cls):
        """
        Получить все продукты, отсортированные по рейтингу с использованием аннотаций.
        """
        products = (
            cls.objects.annotate(
                avg_rating=Avg("reviews__rating"),  # Средний рейтинг на основе отзывов
                max_query=Subquery(
                    cls.objects.filter(category=OuterRef("category")).order_by("-query_count").values("query_count")[:1]
                ),  # Получаем максимальное количество запросов по категории
                normalized_query_count=F("query_count") / F("max_query") * 4,  # Нормализуем количество запросов
            )
            .annotate(weighted_rating=(F("normalized_query_count") + F("avg_rating")) / 2)  # Усредняем запросы и отзывы
            .order_by("-weighted_rating")
        )  # Сортируем по расчетному рейтингу

        return products


class Review(CoreModel):
    """Модель для представления отзыва о товаре"""

    product = models.ForeignKey(
        to=Product,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviews",
        verbose_name=_("User"),
    )
    rating = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        verbose_name=_("Rating"),
    )
    comment = models.TextField(blank=True, verbose_name=_("Comment"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review for {self.product.name} - Rating: {self.rating}"
