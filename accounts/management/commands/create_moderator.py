from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea el grupo Moderador y le asigna permiso para eliminar valoraciones."

    def handle(self, *args, **options):

        permission = Permission.objects.filter(
            content_type__app_label="games",
            codename="delete_gamerating",
        ).first()

        if permission is None:
            raise CommandError(
                "No se encontró el permiso games.delete_gamerating. "
                "Ejecuta primero las migraciones."
            )

        group, created = Group.objects.get_or_create(
            name="Moderador",
        )

        group.permissions.add(
            permission,
        )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    "Grupo Moderador creado correctamente."
                )
            )

        else:

            self.stdout.write(
                self.style.WARNING(
                    "El grupo Moderador ya existe."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Permiso games.delete_gamerating asignado correctamente."
            )
        )