"""
Recommendation Agent — NO GEMINI (rule-based)
Standalone: run from inside agent_recommendation/ folder.
"""
from datetime import datetime, timezone
from fastapi import APIRouter

from data_loader import load_catalog

router = APIRouter(prefix="/recommend/rule", tags=["recommendation-rule"])


def _score(source: dict, candidate: dict) -> tuple[float, str]:
    if candidate["version_id"] == source["version_id"]:
        return 0.0, ""
    if candidate["track_id"] == source["track_id"]:
        return 0.98, "Alternative version within the same parent track family"
    same_genre = bool(set(candidate["genre"]) & set(source["genre"]))
    same_era = abs((candidate["release_year"] or 0) - (source["release_year"] or 0)) <= 3
    if same_genre and same_era:
        return 0.84, f"Matches genre ({', '.join(candidate['genre'])}) and release era"
    if same_genre:
        return 0.6, f"Matches genre ({', '.join(candidate['genre'])})"
    return 0.2, "Weak match — different genre and era"


@router.get("/health")
def health():
    return {"status": "ok", "agent": "recommendation-rule"}


@router.get("/{version_id}")
def recommend(version_id: str, requested_usage: str = "", commercial_only: bool = False):
    catalog = load_catalog()
    source = next((t for t in catalog if t["version_id"] == version_id), None)
    if not source:
        return {"error": "not found", "version_id": version_id}

    candidates = catalog
    if requested_usage:
        candidates = [c for c in candidates if requested_usage in c["usage_types_allowed"]]
    if commercial_only:
        candidates = [c for c in candidates if c["commercial_use"]]

    scored = []
    for c in candidates:
        score, reason = _score(source, c)
        if score > 0:
            scored.append({
                "track_id": c["track_id"], "version_id": c["version_id"],
                "title": c["title"], "artist": c["artist"],
                "display_label": c["display_label"], "version_type": c["version_type"],
                "genre": c["genre"], "release_year": c["release_year"],
                "similarity_score": score, "reason": reason,
            })
    scored.sort(key=lambda x: x["similarity_score"], reverse=True)

    return {
        "recommendation_id": f"rec_rule_{version_id}",
        "source_track_id": source["track_id"],
        "source_version_id": source["version_id"],
        "recommendation_type": "version_substitute",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suggestions": scored[:5],
    }