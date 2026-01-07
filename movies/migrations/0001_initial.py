from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("movie_id", models.IntegerField(unique=True)),
                ("title", models.CharField(max_length=255)),
                ("genres", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="UserRating",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.FloatField()),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "movie",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="user_rating", to="movies.movie"),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
    ]
