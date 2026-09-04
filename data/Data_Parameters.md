# Data Parameters & Schema Reference

## Purpose
Defines the cross-agent parameter matrix and data mapping rules between the **Catalog Agent**, **Version Agent**, **Rights Agent**, and **Recommendation Agent**. This document serves as the master lookup reference to ensure standardized field naming across all services.

## Parameter Matrix Overview

| Original Song (Catalog) | Versions | Rights | Recommendation |
| :--- | :--- | :--- | :--- |
| `track_id` | `version_id` | `master_rights` | `similarity_score` |
| `title` | `title_label` | `publishing_rights` | — |
| `artist` | `version_type` | `composer_rights` | — |
| `aliases` | `artist_label` | `lyricist_rights` | — |
| `genre` | — | `singer_rights` | — |
| `release_year` | — | `rights_type_held` | — |
| — | — | `usage_types_allowed` | — |
| — | — | `commercial_use` | — |
| — | — | `promotional_use` | — |

## Entity Parameter Specs

### 1. Original Song Parameters (Catalog)
*   **`track_id`**: String (`trk_XXX`) — Unique identifier for the parent composition.
*   **`title`**: String — Official title of the core composition.
*   **`artist`**: String — Primary creator/composer of the track.
*   **`aliases`**: Array[String] — Alternative search terms or typo mappings.
*   **`genre`**: Array[String] / String — Musical genre classification tags.
*   **`release_year`**: Integer — Year the original work was first released.

### 2. Version Parameters
*   **`version_id`**: String (`ver_XXX`) — Unique identifier for the specific audio variant.
*   **`title_label`**: String — Display label or version title (e.g., "2024 Remaster").
*   **`version_type`**: Enum — Standardized variant type (`original`, `remaster`, `remix`, `cover`).
*   **`artist_label`**: String — Artist credit line specific to this version.

### 3. Rights Parameters
*   **`master_rights`**: String — Master recording rights holder / label.
*   **`publishing_rights`**: String — Publishing rights holder.
*   **`composer_rights`**: Array[String] — Composer(s) credited for the underlying work.
*   **`lyricist_rights`**: Array[String] — Lyricist(s) credited for the underlying work.
*   **`singer_rights`**: Array[String] — Performer(s)/singer(s) on this version.
*   **`rights_type_held`**: Array[String] — Which rights categories are held (e.g., `master`, `publishing`, `composer`, `lyricist`, `singer`).
*   **`usage_types_allowed`**: Array[String] — Permitted usage contexts (e.g., `movie`, `web series`, `advertisement`, `music video`).
*   **`commercial_use`**: Boolean — Whether commercial use is permitted.
*   **`promotional_use`**: Boolean — Whether use is restricted to promotional-only purposes.

### 4. Recommendation Parameters
*   **`similarity_score`**: Float (`0.0`–`1.0`) — Proximity score relative to the source track/version.

## Notes & Actions
*   **Rights Agent schema is now defined** — the Rights column (`master_rights` through `promotional_use`) has been populated per the P3 schema and no longer pending.
*   **Recommendation Agent schema simplified** — only `similarity_score` is defined at the Recommendation entity level; version-descriptive fields (`title_label`, `artist_label`, `genre_label`, `version_type`) are inherited by reference from the matched Version record rather than duplicated.
