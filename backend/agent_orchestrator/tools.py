"""
Tool functions for the orchestrator agent. Each one is plain Python,
backed by the real dataset. Gemini calls these as "tools" — it decides
which to call, in what order, based on the user's question.
"""
import json
from pathlib import Path
from functools import lru_cache

DATA_PATH = Path(__file__).resolve().parent / "data" / "merged_without_suggest.json"


@lru_cache(maxsize=1)
def _load_catalog() -> list[dict]:
    return json.loads(DATA_PATH.read_text())


def search_catalog(query: str) -> dict:
    """Search the music catalog by track title or artist name.

    Args:
        query: free text — track title, artist name, or partial match.

    Returns:
        Up to 5 matching versions with track_id, version_id, title,
        artist, display_label, version_type.
    """
    catalog = _load_catalog()
    q = query.lower()
    matches = [
        v for v in catalog
        if q in v["title"].lower()
        or q in v["artist"].lower()
        or any(q in a.lower() for a in v.get("aliases", []))
    ]
    return {
        "matches": [
            {
                "track_id": m["track_id"],
                "version_id": m["version_id"],
                "title": m["title"],
                "artist": m["artist"],
                "display_label": m.get("title_label", ""),
                "version_type": m.get("version_type", ""),
            }
            for m in matches[:5]
        ],
        "count": len(matches),
    }


def check_usage_rights(version_id: str, usage_type: str) -> dict:
    """Check whether a specific track version is cleared for a given usage type.

    Args:
        version_id: exact version_id from search_catalog results.
        usage_type: one of e.g. "advertisement", "ott", "trailer", "movie", "social_media".

    Returns:
        Rights breakdown: whether usage is allowed, commercial_use status,
        rights holders, and a clear verdict.
    """
    catalog = _load_catalog()
    entry = next((v for v in catalog if v["version_id"] == version_id), None)
    if not entry:
        return {"error": f"version_id {version_id} not found"}

    allowed_list = entry.get("usage_types_allowed", [])
    is_allowed = usage_type in allowed_list
    commercial_use = entry.get("commercial_use", False)

    return {
        "version_id": version_id,
        "title": entry["title"],
        "display_label": entry.get("title_label", ""),
        "requested_usage": usage_type,
        "usage_allowed": is_allowed,
        "usage_types_allowed": allowed_list,
        "commercial_use": commercial_use,
        "promotional_use": entry.get("promotional_use", False),
        "master_rights_holder": entry.get("master_rights", ""),
        "publishing_rights_holder": entry.get("publishing_rights", ""),
        "verdict": "cleared" if is_allowed else "not_cleared",
    }


def get_alternative_recommendations(version_id: str) -> dict:
    """Suggest alternative track versions when the requested one isn't cleared.

    Args:
        version_id: the version_id that failed rights check.

    Returns:
        Up to 3 alternative versions, scored by similarity, that ARE
        commercially usable.
    """
    catalog = _load_catalog()
    source = next((v for v in catalog if v["version_id"] == version_id), None)
    if not source:
        return {"error": f"version_id {version_id} not found"}

    candidates = [
        v for v in catalog
        if v["version_id"] != version_id and v.get("commercial_use", False)
    ]

    scored = []
    for c in candidates:
        if c["track_id"] == source["track_id"]:
            score, reason = 0.98, "Alternative version of the same track"
        else:
            same_genre = bool(set(c.get("genre", [])) & set(source.get("genre", [])))
            same_era = abs((c.get("release_year") or 0) - (source.get("release_year") or 0)) <= 3
            if same_genre and same_era:
                score, reason = 0.84, "Matches genre and release era"
            elif same_genre:
                score, reason = 0.6, "Matches genre"
            else:
                continue
        scored.append({
            "version_id": c["version_id"],
            "title": c["title"],
            "artist": c["artist"],
            "display_label": c.get("title_label", ""),
            "similarity_score": score,
            "reason": reason,
        })

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return {"alternatives": scored[:3]}


# Registry — maps function name (as Gemini will call it) to the real function
TOOL_REGISTRY = {
    "search_catalog": search_catalog,
    "check_usage_rights": check_usage_rights,
    "get_alternative_recommendations": get_alternative_recommendations,
}