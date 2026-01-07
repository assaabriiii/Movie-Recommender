from django.contrib import admin

from .models import Movie, UserRating


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "movie_id", "genres")
    search_fields = ("title",)


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "rating", "updated_at")
    search_fields = ("movie__title",)
