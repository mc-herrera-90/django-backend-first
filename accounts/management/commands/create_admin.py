from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from decouple import config

class Command(BaseCommand):
    help = "Crea el superadministrador inicial"

    def handle(self, *args, **options):
        User = get_user_model()

        username = config("ADMIN_USERNAME")
        email = config("ADMIN_EMAIL")
        password = config("ADMIN_PASSWORD")

        if not all([username, email, password]):
            self.stderr.write(
                self.style.ERROR(
                    "Faltan las variables ADMIN_USERNAME, ADMIN_EMAIL o ADMIN_PASSWORD."
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("El superadministrador ya existe.")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Superadministrador creado correctamente.")
        )