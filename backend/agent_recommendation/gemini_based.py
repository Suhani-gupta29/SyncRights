"""
Recommendation Agent — WITH GEMINI
Standalone: run from inside agent_recommendation/ folder.
Needs GOOGLE_API_KEY env var + pip install google-genai
"""
import json
import os
from datetime import datetime, timezone
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

from data_loader import load_catalog

router = APIRouter(prefix="/recommend/gemini", tags=["recommendation-gemini"])

_PROMPT = """You are a music-rights recommendation agent.
Given a SOURCE track/version and a list of CANDIDATE versions, rank
the candidates by how good a substitute each is, and write a
one-sentence reason for each.

Return ONLY valid JSON, no markdown fences, no preamble, in this
exact shape:
{{
  "suggestions": [
    {{"version_id": "...", "similarity_score": 0.0, "reason": "..."}}
  ]
}}

SOURCE:
{source}

CANDIDATES:
{candidates}
"""


def _call_gemini(source: dict, candidates: list[dict]) -> list[dict]:
    from google import genai

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    prompt = _PROMPT.format(
        source=json.dumps(source, indent=2),
        candidates=json.dumps(candidates, indent=2),
    )
    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
    text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)["suggestions"]


@router.get("/health")
def health():
    return {"status": "ok", "agent": "recommendation-gemini"}


@router.get("/{version_id}")
def recommend(version_id: str, requested_usage: str = ""):
    catalog = load_catalog()
    source = next((t for t in catalog if t["version_id"] == version_id), None)
    if not source:
        return {"error": "not found", "version_id": version_id}

    candidates = [c for c in catalog if c["version_id"] != version_id]
    if requested_usage:
        candidates = [c for c in candidates if requested_usage in c["usage_types_allowed"]]

    try:
        ranked = _call_gemini(source, candidates)
    except Exception as e:
        return {"error": f"gemini_call_failed: {e}", "fallback": "use /recommend/rule/ instead"}

    by_id = {c["version_id"]: c for c in candidates}
    suggestions = []
    for r in ranked:
        c = by_id.get(r["version_id"])
        if not c:
            continue
        suggestions.append({
            "track_id": c["track_id"], "version_id": c["version_id"],
            "title": c["title"], "artist": c["artist"],
            "display_label": c["display_label"], "version_type": c["version_type"],
            "genre": c["genre"], "release_year": c["release_year"],
            "similarity_score": r["similarity_score"], "reason": r["reason"],
        })

    return {
        "recommendation_id": f"rec_gemini_{version_id}",
        "source_track_id": source["track_id"],
        "source_version_id": source["version_id"],
        "recommendation_type": "version_substitute",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suggestions": suggestions[:5],
    }