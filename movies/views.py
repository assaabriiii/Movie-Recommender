from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RatingForm
from .models import Movie, UserRating
from .services import get_popular_movies, get_rating_stats, get_recommended_movies


def home(request):
    user_ratings = list(UserRating.objects.select_related("movie"))
    user_rating_pairs = [(rating.movie.title, rating.rating) for rating in user_ratings]

    recommendations = []
    popular_movies = []
    error_message = None

    try:
        recommendations = get_recommended_movies(user_rating_pairs)
        if not recommendations:
            popular_movies = get_popular_movies()
    except Exception as exc:
        error_message = f"Recommendation engine error: {exc}"

    context = {
        "recommendations": recommendations,
        "popular_movies": popular_movies,
        "user_ratings": user_ratings,
        "error_message": error_message,
    }
    return render(request, "movies/home.html", context)


def movie_search(request):
    query = request.GET.get("q", "").strip()
    movies = Movie.objects.all()
    if query:
        movies = movies.filter(title__icontains=query).order_by("title")
    else:
        movies = movies.order_by("title")[:60]

    context = {
        "query": query,
        "movies": movies,
    }
    return render(request, "movies/search.html", context)


def movie_detail(request, pk: int):
    movie = get_object_or_404(Movie, pk=pk)
    rating_obj = getattr(movie, "user_rating", None)

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating_obj)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie = movie
            rating.save()
            messages.success(request, "Your rating was saved and recommendations updated.")
            return redirect("movie_detail", pk=movie.pk)
    else:
        form = RatingForm(instance=rating_obj)

    stats = None
    try:
        stats = get_rating_stats(movie.movie_id)
    except Exception:
        stats = None

    context = {
        "movie": movie,
        "form": form,
        "stats": stats,
        "rating_obj": rating_obj,
    }
    return render(request, "movies/detail.html", context)


def watched_movies(request):
    ratings = UserRating.objects.select_related("movie")

    context = {
        "ratings": ratings,
    }
    return render(request, "movies/watched.html", context)
