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

