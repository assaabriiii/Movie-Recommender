import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from movies.models import UserRating
from movies.services import get_popular_movies, get_recommended_movies


class Command(BaseCommand):
    help = "Export a static HTML snapshot for GitHub Pages."

    def handle(self, *args, **options):
        output_dir = Path(settings.BASE_DIR) / "docs"
        css_source = Path(settings.BASE_DIR) / "movies" / "static" / "css" / "styles.css"
        css_target = output_dir / "css" / "styles.css"

        output_dir.mkdir(parents=True, exist_ok=True)
        css_target.parent.mkdir(parents=True, exist_ok=True)

        user_ratings = list(UserRating.objects.select_related("movie"))
        user_rating_pairs = [(rating.movie.title, rating.rating) for rating in user_ratings]

        recommendations = get_recommended_movies(user_rating_pairs)
        if not recommendations:
            popular_movies = get_popular_movies()
        else:
            popular_movies = []

        index_html = render_to_string(
            "movies/static_home.html",
            {
                "recommendations": recommendations,
                "popular_movies": popular_movies,
                "user_ratings": user_ratings,
            },
        )

        watched_html = render_to_string(
            "movies/static_watched.html",
            {"ratings": user_ratings},
        )

        (output_dir / "index.html").write_text(index_html, encoding="utf-8")
        (output_dir / "watched.html").write_text(watched_html, encoding="utf-8")

        if css_source.exists():
            shutil.copy2(css_source, css_target)

        self.stdout.write(self.style.SUCCESS(f"Static site exported to {output_dir}"))
