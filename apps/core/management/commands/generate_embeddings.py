from django.core.management.base import BaseCommand

from apps.assistant.services.embedding import EmbeddingService


class Command(BaseCommand):
    help = "Generate and store embeddings for all products"

    def handle(self, *args, **options):
        self.stdout.write("Starting embedding generation...")
        count = EmbeddingService.generate_and_store_embeddings()
        self.stdout.write(self.style.SUCCESS(f"Successfully generated embeddings for {count} products"))
