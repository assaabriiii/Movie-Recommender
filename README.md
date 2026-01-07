# Movie-Recommender

## Django app setup

1. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and import the MovieLens dataset:

```bash
python manage.py migrate
python manage.py import_movies
```

3. Start the server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` to explore recommendations, search, rate movies, and view watched titles.

## Export a GitHub Pages snapshot

GitHub Pages hosts static sites only, so use the export command to generate `docs/index.html` and `docs/watched.html` with your current recommendations.

```bash
python manage.py export_static
```

Then enable Pages in your repo settings:
- Settings → Pages → Build and deployment
- Source: Deploy from a branch
- Branch: `main` (or `master`) and folder `/docs`

Your static site will be available at `https://<your-username>.github.io/<repo-name>/`.
