# Music Rights Library

A music library frontend focused on **song discovery, music versions, rights information, playlists, and recommendation-oriented exploration**.

The application provides a familiar music-library experience while keeping information about **original songs, variants, artists, genres, years, rights, and usage allowances** accessible.

---

## 📌 Overview

The application is organized around three major sections:

- **Showcase**
- **Stats & Library**
- **Recommendation**

The broader navigation also includes:

- Overview
- All Songs
- ❤️ Liked
- 📚 Playlist
- ➕ Create Playlist

---

# Showcase

The **Showcase** section provides a visual presentation of songs from the dataset.

### Features

- Large song artwork/image.
- Song name displayed on the artwork.
- Artist / master-rights name displayed with the song.
- Songs change using a **right-to-left sliding transition**.
- Manual navigation using:
  - Previous button
  - Next button
- Showcase songs are selected randomly from the dataset.

```text
┌──────────────────────────────────────────────────────┐
│                                                      │
│                   SONG ARTWORK                       │
│                                                      │
│                                                      │
│   Song Name                                          │
│   Artist / Master Rights                             │
│                                             ◀   ▶   │
└──────────────────────────────────────────────────────┘
```

---

# Stats & Library

The **Stats & Library** section contains:

1. Dashboard
2. All Songs
3. Recently Added

It provides both high-level library statistics and multiple ways to browse the music collection.

---

## 📈 Dashboard

The Dashboard provides an overview of the music library.

### Library Statistics

```text
| Statistic      | Description                                        |
|----------------|----------------------------------------------------|
| Total Songs    | Total number of original songs                     |
| Total Genres   | Total number of genres                             |
| Total Artists  | Total artists, counting an original song only once |
| Total Versions | Total number of song versions                      |
```

Below the dashboard, a search bar allows users to search the library.

Search results display:

- Song image
- Song name
- Genre
- Year

Clicking a song opens its details.

---

# Search & Song Details

The search system supports both:

- Original songs
- Variants

---

## Original Song

When the searched song is an **original song**, the detail view displays:

- Song image
- Song name
- ❤️ Like button
- ⋮ More options

### More Options

Users can:

- Add the song to an existing playlist.
- Create a new playlist.

### Song Details

The original song information includes:

- Title
- Genre
- Year
- Artists

### Rights

Rights information includes:

1. Masters
2. Publishing
3. Lyricists

### Usage Information

The interface also displays:

- Allowance to be used
- Commercial usage allowance
- Promotional usage allowance

### Variants

Other versions/variants of the song are displayed below the original song.

Each variant contains:

- Song image
- Song name

Clicking a variant opens its details in a popup.

The popup includes:

- ❤️ Like
- ⋮ More options

---

## Variant

When the searched song is a **variant**, the interface resolves the result to its **original song**.

The original song is displayed with:

- Original song image
- Original song name
- ❤️ Like button
- ⋮ More options

The original song details then include:

- Title
- Genre
- Year
- Artists
- Masters rights
- Publishing rights
- Lyricists
- Allowance to be used
- Commercial usage allowance
- Promotional usage allowance

The interface then displays:

### Other Variants

Variants are displayed using:

- Song image
- Song name

Clicking a variant opens a details popup containing:

- ❤️ Like
- ⋮ More options

### Recommended Songs

Recommended songs are displayed using:

- Song image
- Song name

Clicking a recommended song opens its details popup containing:

- ❤️ Like
- ⋮ More options

---

# All Songs

The **All** section displays the music library according to **genre**.

Each genre is represented as a toggle/section.

---

## Genre View

The closed genre view displays a maximum of **5 original songs**.

Each song contains:

- Song image
- Song name

Clicking a song opens its details popup.

The popup provides:

- ❤️ Like
- ⋮ More options

Each genre also provides a:

**View All** button.

---

## Expanded Genre

When a genre is opened:

- The complete collection for that genre is displayed.
- A search bar is provided.
- Songs are displayed using:
  - Song image
  - Song name
- Clicking a song opens its details popup.
- The popup provides Like and More Options functionality.

```text
Genre
────────────────────────────────────────────

[Song] [Song] [Song] [Song] [Song]  View All
```

---

# Recently Added

The **Recently Added** section organizes songs according to **year**.

Years are displayed in descending order.

Each year is represented as a toggle/section.

---

## Year View

The closed year view displays a maximum of **5 original songs**.

Each song contains:

- Song image
- Song name

Clicking a song opens its details popup.

The popup provides:

- ❤️ Like
- ⋮ More options

Each year also provides a:

**View All** button.

---

## Expanded Year

When a year is opened:

- The complete collection for that year is displayed.
- A search bar is provided.
- Songs are displayed using:
  - Song image
  - Song name
- Clicking a song opens its details popup.
- The popup provides Like and More Options functionality.

---

## Timeline

A timeline scroller is provided for quick navigation through years.

The timeline is available in:

- Closed year sections
- Expanded year sections

This allows users to quickly move between different years in the library.

---

# Recommendation

The **Recommendation** section is a dedicated area for song discovery.

Recommendations are also presented within individual song details.

A recommended song is displayed using:

- Song image
- Song name

Clicking the recommended song opens a popup containing:

- ❤️ Like
- ⋮ More options

> **Note:** The uploaded specification introduces the Recommendation section but does not define the detailed recommendation algorithm, ranking logic, or recommendation criteria. Those details can be connected to the recommendation dataset/engine separately.

---

# Navigation

The sidebar provides the primary application navigation.

```text
┌─────────────────────────┐
│ Music Rights Library    │
├─────────────────────────┤
│ Overview                │
│ All Songs               │
│ ❤️ Liked                │
│ 📚 Playlist             │
│                         │
│ ➕ Create Playlist      │
└─────────────────────────┘
```

### Navigation Options

#### Overview

Main dashboard containing:

- Showcase
- Stats & Library
- Recommendation

#### All Songs

Browse the complete song library organized by genre.

#### Liked

Access songs added to the user's liked collection.

#### Playlist

Access existing playlists.

#### Create Playlist

Create a new playlist.

---

# Global Controls

The top section of the interface provides global controls.

## Search

Search through the music library.

## Filter

Filtering options include:

- Genre
- Year
- Artist

## Showcase Ordering

The Showcase provides ordering controls:

- Ascending
- Descending

---

## Summary

```text
┌────────────────────────────────────────────────────────┐
│                  MUSIC RIGHTS LIBRARY                  │
├────────────────────────────────────────────────────────┤
│                                                        │
│  SHOWCASE                                              │
│  └── Random Songs • Slider • Navigation                │
│                                                        │
│  STATS & LIBRARY                                       │
│  ├── Dashboard                                         │
│  │   ├── Total Songs                                   │
│  │   ├── Total Genres                                  │
│  │   ├── Total Artists                                 │
│  │   └── Total Versions                                │
│  │                                                     │
│  ├── All                                               │
│  │   └── Genre-based Library                           │
│  │                                                     │
│  └── Recently Added                                    │
│      └── Year-based Library + Timeline                 │
│                                                        │
│  RECOMMENDATION                                        │
│  └── Recommended Songs                                 │
│                                                        │
├────────────────────────────────────────────────────────┤
│  Overview                                              |
|  All Songs                                             |
|  ❤️ Liked  Playlist                                    │
│  ➕ Create Playlist                                    │
└────────────────────────────────────────────────────────┘
```

**Music → Rights → Versions → Discovery → Recommendations**