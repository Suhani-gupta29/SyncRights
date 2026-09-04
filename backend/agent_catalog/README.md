\# Catalog Agent



\## Purpose

Given a free-text search query, find matching track(s) in the seed catalog.



\## Input

\- query\_text: string (e.g. "Example Song", "example song 1998")



\## Output

\- List of matching track objects (shape defined in /SCHEMA.md under "Track")

\- Empty list if no match found



\## Planned endpoint

GET /search?q={query\_text}



\## Notes

\- Matching should tolerate typos/partial matches (e.g. "exmple song" should still find "Example Song")

\- Multiple matches are possible if the query is ambiguous (e.g. searching by artist name only)

\- Relies on `aliases` field in Track schema for fuzzy matching




## Day 9 — Gemini Query Cleaning

The Catalog Agent uses Gemini to clean conversational and natural-language
queries before passing them to the existing RapidFuzz search layer.

### Search Pipeline

User query
    ↓
Gemini query cleaning
    ↓
clean_query
    ↓
RapidFuzz fuzzy search
    ↓
data/seed_data.json
    ↓
matching tracks

Gemini is responsible only for query cleaning.

It does not:
- select catalog tracks
- determine the final search result
- replace the RapidFuzz search layer

### Fallback

If Gemini is unavailable or the Gemini request fails, the original user
query is passed to RapidFuzz.

This allows catalog search to continue even when the Gemini service is
temporarily unavailable.

### Environment Variable

The Gemini API key is provided through:

GEMINI_API_KEY

The API key is stored in the local `.env` file and as an environment
variable in production. It is never committed to Git.

