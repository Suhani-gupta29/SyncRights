# Rights Intelligence Agent (P3)

## Pipeline Overview & Workflow
The Rights Agent is a critical bridge in the music compliance and intelligence pipeline:
1. **Upstream Dependency:** It receives catalog and version details (such as `track_id` and `version_id`) from the upstream Catalog and Version agents.
2. **Rights & Ownership Processing:** It queries the domestic data store to evaluate the master owner, publishing owner, and active synchronization license details exclusively for the Indian market.
3. **Downstream Integration (Recommendation Agent):** Once rights, ownership, and sync clearance statuses are verified, the Rights Agent passes its evaluation data downstream to the **Recommendation Agent**. 
4. **Alternative Processing:** If a requested version lacks appropriate sync clearance or rights ownership, the Recommendation Agent uses this output to suggest valid alternative versions or similar tracks from the same track family based on similarity scores and metadata matching.

## Input
- `track_id`: string (e.g., `trk_001`)
- `version_id`: string (e.g., `ver_001`)

## Output
- Returns structured ownership metadata, including master and publishing entities, alongside synchronization license statuses and expiration timelines for the requested version, formatted for consumption by downstream compliance and recommendation services.

## Endpoint (planned)
`GET /rights/{track_id}/{version_id}`