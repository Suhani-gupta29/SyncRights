import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rapidfuzz import fuzz


app = FastAPI(title="SyncRights Catalog Agent")


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Load catalog data
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "seed_data.json"

try:
    with open(DATA_FILE, encoding="utf-8") as f:
        seed_data = json.load(f)

    tracks = seed_data["tracks"]

    print(f"Loaded {len(tracks)} tracks from {DATA_FILE}")

except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
    tracks = []
    print(f"Warning: failed to load seed data: {e}")


# --------------------------------------------------
# Search helpers
# --------------------------------------------------

def normalize_text(text: str) -> str:
    """Normalize text for case-insensitive searching."""
    return " ".join(text.lower().strip().split())


def calculate_track_score(query: str, track: dict) -> float:
    """
    Calculate a relevance score for a track.

    Search fields:
    - title
    - artist
    - aliases

    Exact and substring matches are prioritized over
    fuzzy matches to reduce irrelevant results.
    """

    title = normalize_text(track.get("title", ""))
    artist = normalize_text(track.get("artist", ""))

    aliases = [
        normalize_text(alias)
        for alias in track.get("aliases", [])
    ]

    # --------------------------------------------------
    # Exact matches
    # --------------------------------------------------

    if query == title:
        return 100

    if query == artist:
        return 100

    if query in aliases:
        return 100

    # --------------------------------------------------
    # Direct substring matches
    # --------------------------------------------------

    if query in title:
        return 95

    if query in artist:
        return 95

    if any(query in alias for alias in aliases):
        return 95

    # --------------------------------------------------
    # Fuzzy matching
    # --------------------------------------------------

    title_score = fuzz.ratio(query, title)
    artist_score = fuzz.ratio(query, artist)

    alias_score = 0

    if aliases:
        alias_score = max(
            fuzz.ratio(query, alias)
            for alias in aliases
        )

    return max(
        title_score,
        artist_score,
        alias_score
    )


def search_tracks(query: str, threshold: int = 70):
    """
    Search the catalog using title, artist and aliases.

    Results are ordered from strongest match
    to weakest match.
    """

    query = normalize_text(query)

    if not query:
        return []

    results = []

    for track in tracks:
        score = calculate_track_score(query, track)

        if score >= threshold:
            results.append((score, track))

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [track for score, track in results]


# --------------------------------------------------
# API endpoints
# --------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(q: str = ""):
    return search_tracks(q)