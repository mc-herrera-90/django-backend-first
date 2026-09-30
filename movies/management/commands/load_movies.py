import json
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Carga las películas desde movies.json."

    def handle(self, *args, **options):
        json_path = (
            Path(__file__).resolve().parents[2]
            / "static"
            / "data"
            / "movies.json"
        )

        if not json_path.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"No se encontró el archivo: {json_path}"
                )
            )
            return

        with json_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            movies = json.load(file)

        created = 0
        updated = 0

        for movie_data in movies:
            movie, was_created = Movie.objects.update_or_create(
                title=movie_data["title"],
                year=movie_data["year"],
                defaults={
                    "genre": movie_data["genre"],
                    "director": movie_data["director"],
                    "duration": movie_data["duration"],
                    "country": movie_data["country"],
                    "language": movie_data["language"],
                    "studio": movie_data["studio"],
                    "description": movie_data["description"],
                    "cast": ", ".join(
                        movie_data.get("cast", [])
                    ),
                },
            )

            self._load_image(
                movie,
                movie_data.get("portrait"),
                "portrait",
            )

            self._load_image(
                movie,
                movie_data.get("landscape"),
                "landscape",
            )

            self._load_trailer(
                movie,
                movie_data.get("trailer"),
            )

            movie.save()

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Películas creadas: {created}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Películas actualizadas: {updated}"
            )
        )

    def _load_image(self, movie, path, field_name):
        if not path:
            return

        file_path = Path(path)

        if not file_path.is_absolute():
            file_path = (
                Path(__file__).resolve().parents[2]
                / "static"
                / path
            )

        if not file_path.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No se encontró {field_name}: {file_path}"
                )
            )
            return

        field = getattr(movie, field_name)

        if field:
            return

        with file_path.open("rb") as file:
            field.save(
                file_path.name,
                File(file),
                save=False,
            )

    def _load_trailer(self, movie, path):
        if not path:
            return

        file_path = Path(path)

        if not file_path.is_absolute():
            file_path = (
                Path(__file__).resolve().parents[2]
                / "static"
                / path
            )

        if not file_path.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"No se encontró trailer: {file_path}"
                )
            )
            return

        if movie.trailer:
            return

        with file_path.open("rb") as file:
            movie.trailer.save(
                file_path.name,
                File(file),
                save=False,
            )