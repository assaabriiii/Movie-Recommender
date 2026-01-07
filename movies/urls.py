from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.movie_search, name="movie_search"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("watched/", views.watched_movies, name="watched_movies"),
]
