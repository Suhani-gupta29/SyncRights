"""
Data loader — reads data/merged_without_suggest.json
Real confirmed shape: flat list, 240 entries (80 tracks x 3 versions),
one object per version, already merged tracks+versions+rights.

No sync_license_granted field exists in this dataset — using
usage_types_allowed + commercial_use as the real licensing signal
instead. Ignoring the pre-existing "similarity_score" field in the
raw data — it looks like static leftover noise (near-identical per
row), not a real pairwise score; scorers compute their own.
"""
import json
from pathlib import Path
from functools import lru_cache

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "merged_without_suggest.json"


@lru_cache(maxsize=1)
def load_catalog() -> list[dict]:
    raw = json.loads(DATA_PATH.read_text())

    flat = []
    for v in raw:
        flat.append({
            "track_id": v["track_id"],
            "version_id": v["version_id"],
            "title": v["title"],
            "artist": v["artist"],
            "display_label": v.get("title_label", ""),
            "version_type": v.get("version_type", ""),
            "genre": v.get("genre", []),
            "release_year": v.get("release_year"),
            "usage_types_allowed": v.get("usage_types_allowed", []),
            "commercial_use": v.get("commercial_use", False),
            "promotional_use": v.get("promotional_use", False),
        })
    return flat