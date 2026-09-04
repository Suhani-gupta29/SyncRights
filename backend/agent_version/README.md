# Version Intelligence Agent

## Purpose
Given a specific `track_id` and an optional free-text context (like "remix" or "2024"), identify and return the exact matching version object for that track.

## Input
- track_id: string (required, e.g. "trk_001")
- version_query: string (optional, e.g. "Club Remix", "remastered", "acoustic")

## Output
- A single Version object (shape defined in /SCHEMA.md under "Version Schema")
- Returns null or a 404 error if the requested version doesn't exist for the given track

## Planned endpoint
GET /versions/match?track_id={track_id}&q={version_query}

## Notes
- If `version_query` is not provided by the user, the agent should intelligently default to returning the `version_type: "original"`.
- Relies on `display_label`, `version_type`, and `featured_artists` to disambiguate if multiple remixes or remasters exist.
- It acts as the bridge: it takes the Track ID from the Catalog Agent and gives the exact Version ID to the Rights Agent.
