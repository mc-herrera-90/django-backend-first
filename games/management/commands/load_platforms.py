from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from games.models import Platform


class Command(BaseCommand):
    help = "Carga las plataformas desde los iconos disponibles."

    PLATFORM_NAMES = {
        "gba": "Game Boy Advance",
        "n64": "Nintendo 64",
        "neogeo": "Neo Geo",
        "nes": "Nintendo Entertainment System",
        "snes": "Super Nintendo Entertainment System",
    }

    def handle(self, *args, **options):
        platforms_path = (
            Path(settings.BASE_DIR)
            / "games"
            / "static"
            / "img"
            / "platforms"
        )

        if not platforms_path.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"No existe el directorio: {platforms_path}"
                )
            )
            return

        created = 0
        updated = 0

        for icon_path in sorted(platforms_path.iterdir()):

            if not icon_path.is_file():
                continue

            identifier = icon_path.stem.lower()

            name = self.PLATFORM_NAMES.get(
                identifier,
                identifier.replace("-", " ").replace("_", " ").title(),
            )

            platform, was_created = Platform.objects.get_or_create(
                identifier=identifier,
                defaults={
                    "name": name,
                },
            )

            with icon_path.open("rb") as icon_file:
                platform.icon.save(
                    icon_path.name,
                    File(icon_file),
                    save=True,
                )

            if was_created:
                created += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Creada: {name} ({identifier})"
                    )
                )
            else:
                updated += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Actualizada: {name} ({identifier})"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso completado: {created} creadas, "
                f"{updated} actualizadas."
            )
        )