from django.db import models

from apps.core.models import CoreModel
from apps.product.models import Product


class ProductEmbedding(CoreModel):
    """Stores embeddings for products to enable semantic search"""

    product = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
        related_name="embedding",
    )
    embedding_vector = models.JSONField(help_text="Embedding vector from OpenAI")

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"Embedding for {self.product.name}"
