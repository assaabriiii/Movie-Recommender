import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = "Import MovieLens movies into the database."

    def handle(self, *args, **options):
        movies_path = settings.DATA_DIR / "movies.csv"
        if not movies_path.exists():
            self.stderr.write(self.style.ERROR(f"Missing dataset file: {movies_path}"))
            return

        created = 0
        updated = 0

        with movies_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                movie_id = int(row["movieId"])
                defaults = {
                    "title": row["title"],
                    "genres": row.get("genres", ""),
                }
                _, was_created = Movie.objects.update_or_create(
                    movie_id=movie_id,
                    defaults=defaults,
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f"Imported movies. Created: {created}, Updated: {updated}"))
