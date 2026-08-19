## Data Schemas

### 1. Catalog Agent Schema
Defines the primary track entity and stores reference IDs for associated versions.

```json
{
  "track_id": "trk_001",
  "title": "Example Song",
  "artist": "Example Artist",
  "aliases": ["Exampl Song"],
  "genre": ["pop"],
  "release_year": 1998,
  "versions": ["ver_001", "ver_002", "ver_003"]
}
```

### 2. Version Intelligence Schema
Enriches version reference IDs with specific attributes such as remasters, remixes, and featured collaborators.

```json
{
  "track_id": "trk_001",
  "title": "Example Song",
  "artist": "Example Artist",
  "aliases": [
    "Exampl Song",
    "Exmpl Song"
  ],
  "genre": [
    "pop"
  ],
  "release_year": 1998,
  "versions": [
    {
      "version_id": "ver_001",
      "display_label": "Original Studio Recording",
      "version_type": "original",
      "featured_artists": []
    },
    {
      "version_id": "ver_002",
      "display_label": "2024 Remastered Version",
      "version_type": "remaster",
      "featured_artists": []
    },
    {
      "version_id": "ver_003",
      "display_label": "Club Remix (feat. DJ Sample)",
      "version_type": "remix",
      "featured_artists": [
        "DJ Sample"
      ]
    }
  ]
}
```

### 3. Rights
Tracks master rights, publishing ownership, sync licensing status, and expiration dates per specific version.

```json
{
  "track_id": "trk_001",
  "versions_rights": [
    {
      "version_id": "ver_001",
      "display_label": "Original Studio Recording",
      "version_type": "original",
      "master_owner": "XYZ Records India",
      "publishing_owner": "ABC Publishing India",
      "sync_license_granted": false,
      "sync_license_expiry": null
    },
    {
      "version_id": "ver_002",
      "display_label": "2024 Remastered Version",
      "version_type": "remaster",
      "master_owner": "XYZ Records India",
      "publishing_owner": "ABC Publishing India",
      "sync_license_granted": false,
      "sync_license_expiry": null
    },
    {
      "version_id": "ver_003",
      "display_label": "Club Remix (feat. DJ Sample)",
      "version_type": "remix",
      "master_owner": "XYZ Records & Remix Hub India",
      "publishing_owner": "ABC Publishing & DJ Sample Music",
      "sync_license_granted": true,
      "sync_license_expiry": "2027-12-31T23:59:59Z"
    }
  ]
}
```

### 4. Recommendation
Outputs ranked alternative choices (intra-track versions or similar external tracks) based on metadata matches and similarity scores.

```json
{
  "recommendation_id": "rec_001",
  "source_track_id": "trk_001",
  "source_version_id": "ver_002",
  "recommendation_type": "version_substitute",
  "timestamp": "2026-08-19T21:44:00Z",
  "suggestions": [
    {
      "track_id": "trk_001",
      "version_id": "ver_001",
      "title": "Example Song",
      "artist": "Example Artist",
      "display_label": "Original Studio Recording",
      "version_type": "original",
      "genre": ["pop"],
      "release_year": 1998,
      "similarity_score": 0.98,
      "reason": "Alternative version within the same parent track family"
    },
    {
      "track_id": "trk_042",
      "version_id": "ver_108",
      "title": "Similar Synth Hit",
      "artist": "Another Artist",
      "display_label": "2020 Remaster",
      "version_type": "remaster",
      "genre": ["pop"],
      "release_year": 1998,
      "similarity_score": 0.84,
      "reason": "Matches genre (pop), release era (1998), and acoustic profile"
    }
  ]
}
```
