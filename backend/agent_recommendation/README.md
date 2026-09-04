# Recommendation Agent

## Purpose
Given a source track and version ID, generate a ranked list of alternative versions or metadata-similar tracks.

## Input
- source_track_id: string (required, e.g. "trk_001")
- source_version_id: string (optional, e.g. "ver_002")
- recommendation_type: string (optional enum: "version_substitute", "similar_track", "catalog_fallback"; default: "version_substitute")
- limit: integer (optional, default: 5)

## Output
- A single Recommendation object containing ranked `suggestions` (shape defined in /SCHEMA.md under "Recommendation")
- Returns an empty `suggestions` list if no matching alternatives exist

## Planned endpoint
GET /recommendations?track_id={source_track_id}&version_id={source_version_id}&type={recommendation_type}

## Notes
- `version_substitute` prioritizes alternate recordings belonging to the exact same parent `track_id` (e.g. suggesting "ver_001" when "ver_002" is selected).
- `similar_track` matches candidates based on shared `genre`, release era (`release_year`), and artist similarity.
- `similarity_score` must be a normalized float between `0.0` and `1.0`.
- Serves as the primary fallback engine when the Compliance Agent (P4) flags a requested track version as blocked or restricted.

## Render Trial Links
- https://syncrights-recommendation.onrender.com/health
- https://syncrights-recommendation.onrender.com/recommend/rule/ver_042_a
- https://syncrights-recommendation.onrender.com/recommend/gemini/ver_042_a
- https://syncrights-recommendation.onrender.com/recommend/rule/ver_042_a?requested_usage=advertisement&commercial_only=true