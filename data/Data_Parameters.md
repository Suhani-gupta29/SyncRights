# Data Parameters & Schema Reference

## Purpose
Defines the cross-agent parameter matrix and data mapping rules between the **Catalog Agent**, **Version Agent**, **Rights Agent**, and **Recommendation Agent**. This document serves as the master lookup reference to ensure standardized field naming across all services.

## Parameter Matrix Overview

| Original Song (Catalog) | Versions | Rights | Recommendation |
| :--- | :--- | :--- | :--- |
| `track_id` | `version_id` | *(Pending Definition)* | `version_id` |
| `title` | `title_label` | *""* | `title_label` |
| `artist` | `artist_label` | *""* | `artist_label` |
| `aliases` | — | — | — |
| `genre` | `genre_label` | *""* | `genre_label` |
| `release_year` | — | *""* | — |
| — | `version_type` | *""* | `version_type` |
| — | — | *""* | `similarity_score` |

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
*   **`artist_label`**: String — Artist credit line specific to this version.
*   **`genre_label`**: String — Genre designation specific to this version variant.
*   **`version_type`**: Enum — Standardized variant type (`original`, `remaster`, `remix`, `cover`).

### 3. Rights Parameters
*   *Status*: Unmapped / Pending schema definition from P3 (Rights Intelligence Agent).

### 4. Recommendation Parameters
*   **`version_id`**: String (`ver_XXX`) — Target recommended version identifier.
*   **`title_label`**: String — Display title of the suggested track version.
*   **`artist_label`**: String — Display artist name of the suggested version.
*   **`genre_label`**: String — Genre tag for recommendation sorting/filtering.
*   **`version_type`**: Enum — Variant category of the suggested track.
*   **`similarity_score`**: Float (`0.0`–`1.0`) — Proximity score relative to the source track.

## Notes & Actions
*   **Rights Agent Action Item**: P3 needs to populate the `Rights` column with master ownership, publishing, territory, and sync license fields.