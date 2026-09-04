import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel
from rapidfuzz import fuzz


# --------------------------------------------------
# Environment configuration
# --------------------------------------------------

# Load variables from .env during local development.
# On Render, environment variables are provided directly
# by the platform.
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    print("Gemini client configured.")
else:
    gemini_client = None
    print("Warning: GEMINI_API_KEY not configured. Gemini query cleaning is disabled.")


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(title="SyncRights Catalog Agent")


# --------------------------------------------------
# CORS configuration
# --------------------------------------------------

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
# Gemini structured output
# --------------------------------------------------

class QueryCleaningResult(BaseModel):
    clean_query: str


# --------------------------------------------------
# Gemini query-cleaning prompt
# --------------------------------------------------

QUERY_CLEANING_PROMPT = """
You are the query-cleaning component of a music catalog search system.

Your only task is to convert the user's search query into the shortest useful
search phrase for fuzzy catalog search.

The result should ideally contain:
- a track title
- an artist name
- an alias
- or another concise phrase useful for catalog search

Rules:
1. Do not answer the user's question.
2. Do not explain your reasoning.
3. Do not select a track.
4. Do not invent artists, titles, or facts.
5. Preserve meaningful names and words from the user's query.
6. If the query is already a clean title or artist name, return it unchanged.
7. If the query is conversational, remove unnecessary conversational wording.
8. If no useful cleaning is possible, return the original query unchanged.
"""


# --------------------------------------------------
# Gemini query cleaner
# --------------------------------------------------

def clean_query_with_gemini(query: str) -> str:
    """
    Clean a natural-language search query using Gemini.

    Gemini is only responsible for converting a conversational
    query into a concise search phrase.

    If Gemini is unavailable or fails for any reason,
    the original query is returned so that RapidFuzz can
    continue searching normally.
    """

    # Do not call Gemini for an empty query.
    if not query.strip():
        return query

    # If Gemini is not configured, use the original query.
    if gemini_client is None:
        return query

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""
{QUERY_CLEANING_PROMPT}

User query:
{query}
""",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=QueryCleaningResult,
                temperature=0,
            ),
        )

        # The SDK parses the structured response according to
        # the Pydantic schema.
        result = response.parsed

        if result and result.clean_query.strip():
            clean_query = result.clean_query.strip()

            print(
                f"Gemini query cleaning: "
                f"'{query}' -> '{clean_query}'"
            )

            return clean_query

        # If Gemini returns an empty result, use original query.
        print(
            "Warning: Gemini returned an empty clean_query. "
            "Using original query."
        )

        return query

    except Exception as e:
        # Gemini is an enhancement, not a hard dependency.
        # RapidFuzz should still work if Gemini fails.
        print(f"Warning: Gemini query cleaning failed: {e}")
        print("Falling back to original query.")

        return query


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
    """
    Search the catalog.

    Pipeline:

    User query
        ↓
    Gemini query cleaning
        ↓
    clean_query
        ↓
    RapidFuzz
        ↓
    catalog results

    If Gemini fails, the original query is passed
    directly to RapidFuzz.
    """

    # Avoid unnecessary Gemini calls for empty queries.
    if not q.strip():
        return []

    # Gemini cleans conversational/natural-language queries.
    clean_query = clean_query_with_gemini(q)

    # Existing Day 8 RapidFuzz search remains responsible
    # for actually finding catalog tracks.
    return search_tracks(clean_query)