from __future__ import annotations

from functools import lru_cache

import pandas as pd
from django.conf import settings

from .models import Movie


@lru_cache(maxsize=1)
def _load_dataset():
    movies_path = settings.DATA_DIR / "movies.csv"
    ratings_path = settings.DATA_DIR / "ratings.csv"

    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    df = pd.merge(ratings_df, movies_df, on="movieId")

    rating_count = df.groupby("title")["rating"].count()
    popular_titles = rating_count[rating_count > 100].index

    movie_matrix = df.pivot_table(index="userId", columns="title", values="rating")
    movie_matrix = movie_matrix[popular_titles]

    rating_stats = df.groupby("movieId")["rating"].agg(["mean", "count"]).rename(
        columns={"mean": "avg_rating", "count": "rating_count"}
    )

    return movie_matrix, rating_count.sort_values(ascending=False), rating_stats


def _ordered_movies_from_titles(titles: list[str]) -> list[Movie]:
    if not titles:
        return []
    title_set = set(titles)
    movies = Movie.objects.filter(title__in=title_set)
    movie_map = {movie.title: movie for movie in movies}
    return [movie_map[title] for title in titles if title in movie_map]


def get_popular_movies(limit: int = 12) -> list[Movie]:
    _, rating_count, _ = _load_dataset()
    titles = rating_count.head(limit).index.tolist()
    return _ordered_movies_from_titles(titles)


def get_recommended_movies(user_ratings: list[tuple[str, float]], limit: int = 12) -> list[Movie]:
    movie_matrix, _, _ = _load_dataset()

    if not user_ratings:
        return []

    similar_movies = []
    for title, rating in user_ratings:
        if title not in movie_matrix.columns:
            continue
        corr_scores = movie_matrix.corrwith(movie_matrix[title])
        weighted_scores = corr_scores * (rating - 2.5)
        similar_movies.append(weighted_scores)

    if not similar_movies:
        return []

    final_scores = pd.concat(similar_movies, axis=1).sum(axis=1)
    final_scores = final_scores.sort_values(ascending=False)
    watched_titles = [title for title, _ in user_ratings]
    final_scores = final_scores.drop(watched_titles, errors="ignore")

    titles = final_scores.head(limit).index.tolist()
    return _ordered_movies_from_titles(titles)


def get_rating_stats(movie_id: int) -> dict[str, float | int] | None:
    _, _, rating_stats = _load_dataset()
    if movie_id not in rating_stats.index:
        return None
    stats = rating_stats.loc[movie_id]
    return {"avg_rating": float(stats["avg_rating"]), "rating_count": int(stats["rating_count"])}
