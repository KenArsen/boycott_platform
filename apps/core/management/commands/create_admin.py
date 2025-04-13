from django.core.management.base import BaseCommand

from apps.account.models import User


class Command(BaseCommand):
    help = "Creates a default superuser"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(email="admin@gmail.com").exists():
            User.objects.create_superuser(
                email="admin@gmail.com",
                password="admin",
                first_name="Admin",
                last_name="Admin",
                phone_number="0 (XXX) XX XX XX",
                is_email_verified=True,
            )
            self.stdout.write(self.style.SUCCESS("Superuser created: admin@gmail.com / admin"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
