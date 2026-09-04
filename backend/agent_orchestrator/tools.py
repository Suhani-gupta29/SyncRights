"""
The REAL Pipeline Tools — Wired with P1, P2, P3, and P4 Agents.
"""
import sys
import os

# Python path magic taaki hum baaki folders se code import kar sakein
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)

# Backend root ko path mein add karo
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# P4 (Recommendation) ke folder ko bhi path mein add karo taaki wo apna 'data_loader' dhoondh sake
p4_dir = os.path.join(backend_dir, "agent_recommendation")
if p4_dir not in sys.path:
    sys.path.append(p4_dir)

# --------------------------------------------------
# Importing all 4 Real Agents!
# --------------------------------------------------
from agent_catalog.main import search as p1_search
from agent_version.ai_matcher import match_version_with_ai as p2_match
from agent_rights.lookup import get_rights_data as p3_lookup
from agent_recommendation.rule_based import recommend as p4_recommend

# ... (Baaki neeche ka code jaise pehle tha waise hi rehne de) ...

def search_catalog(query: str) -> dict:
    """P1 + P2: Search catalog AND find the exact version."""

    # STEP 1: P1 finds the track
    tracks = p1_search(q=query)

    if not tracks:
        return {"error": f"No tracks found for query: {query}"}

    # Top track found by P1 Catalog Agent
    top_track = tracks[0]
    top_track_id = top_track["track_id"]

    # Extract P1 catalog metadata safely
    track_title = (
        top_track.get("title")
        or top_track.get("track_title")
        or top_track.get("name")
        or ""
    )

    track_artist = (
        top_track.get("artist")
        or top_track.get("artist_name")
        or ""
    )

    # STEP 2: P2 finds the exact AI version match
    p2_result = p2_match(
        track_id=top_track_id,
        user_query=query
    )

    if p2_result.get("status") == "success":
        return {
            "matches": [
                {
                    "track_id": p2_result.get(
                        "track_id",
                        top_track_id
                    ),
                    "version_id": p2_result.get(
                        "matched_version_id",
                        ""
                    ),

                    # Existing P2 fields preserved
                    "title_label": p2_result.get(
                        "title_label",
                        ""
                    ),
                    "version_type": p2_result.get(
                        "version_type",
                        ""
                    ),
                    "ai_reasoning": p2_result.get(
                        "ai_reasoning",
                        ""
                    ),

                    # P1 Day 13 logging fields added
                    "title": track_title,
                    "artist": track_artist,
                }
            ],
            "count": 1
        }

    return {
        "error": p2_result.get(
            "message",
            "Version match failed."
        )
    }

def check_usage_rights(version_id: str, usage_type: str) -> dict:
    """P3: Sanket's logic for fetching exact rights."""
    
    # STEP 3: P3 (Sanket) fetches rights
    rights = p3_lookup(version_id=version_id)
    if rights.get("status") == "error":
        return {"error": rights.get("message")}
        
    allowed_list = rights.get("usage_types_allowed", [])
    is_allowed = usage_type.lower() in [u.lower() for u in allowed_list]
    
    return {
        "version_id": version_id,
        "title": rights.get("title"),
        "requested_usage": usage_type,
        "usage_allowed": is_allowed,
        "usage_types_allowed": allowed_list,
        "commercial_use": rights.get("commercial_use"),
        "master_rights_holder": rights.get("master_rights", ""),
        "publishing_rights_holder": rights.get("publishing_rights", ""),
        "verdict": "cleared" if is_allowed else "not_cleared",
    }

def get_alternative_recommendations(version_id: str) -> dict:
    """P4: Rule-based alternative suggestions."""
    
    # STEP 4: P4 fetches alternatives
    rec_result = p4_recommend(version_id=version_id, commercial_only=True)
    
    return {
        "alternatives": rec_result.get("suggestions", [])[:3] 
    }

# Registry — maps function name to our newly wired functions
TOOL_REGISTRY = {
    "search_catalog": search_catalog,
    "check_usage_rights": check_usage_rights,
    "get_alternative_recommendations": get_alternative_recommendations,
}