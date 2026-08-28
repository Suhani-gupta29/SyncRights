"use client";

import { useEffect, useMemo, useState } from "react";

import {
  ShieldCheck,
  Search,
  LayoutGrid,
  Music2,
  Heart,
  ListMusic,
  Plus,
  SlidersHorizontal,
  ChevronLeft,
  ChevronRight,
  ArrowUpNarrowWide,
  ArrowDownNarrowWide,
  Disc3,
  Tags,
  UserRound,
  FileCheck2,
  Heart as HeartIcon,
  MoreVertical,
  X,
  LockKeyhole,
  CheckCircle2,
  XCircle,
  ListPlus,
  CalendarDays,
} from "lucide-react";

const NAV_ITEMS = [
  { id: "overview", label: "Overview", icon: LayoutGrid },
  { id: "all-songs", label: "All Songs", icon: Music2 },
  { id: "liked", label: "Liked", icon: Heart },
  { id: "playlist", label: "Playlist", icon: ListMusic },
];

const SONGS = [
  {
    id: "s1",
    name: "Blinding Lights",
    artist: "The Weeknd",
    genre: "Synthwave",
    year: 2019,
    rights: {
      masters: "Republic Records",
      publishing: "Universal Music Publishing",
      lyricists: ["Abel Tesfaye", "Max Martin"],
    },
    usage: { allowance: "62% used", commercial: "Allowed", promotional: "Allowed" },
    versions: [
      { id: "s1-v1", name: "Original Version" },
      { id: "s1-v2", name: "Live Version" },
      { id: "s1-v3", name: "Instrumental" },
    ],
  },
  {
    id: "s2",
    name: "Levitating",
    artist: "Dua Lipa",
    genre: "Dance",
    year: 2020,
    rights: {
      masters: "Warner Records",
      publishing: "Warner Chappell Music",
      lyricists: ["Dua Lipa", "Clarence Coffee Jr."],
    },
    usage: { allowance: "35% used", commercial: "Allowed", promotional: "Allowed" },
    versions: [
      { id: "s2-v1", name: "Album Version" },
      { id: "s2-v2", name: "Remix Version" },
    ],
  },
  {
    id: "s3",
    name: "Shape of You",
    artist: "Ed Sheeran",
    genre: "Pop",
    year: 2017,
    rights: {
      masters: "Asylum Records",
      publishing: "Sony Music Publishing",
      lyricists: ["Ed Sheeran", "Steve Mac"],
    },
    usage: { allowance: "80% used", commercial: "Restricted", promotional: "Allowed" },
    versions: [
      { id: "s3-v1", name: "Original Version" },
      { id: "s3-v2", name: "Acoustic Version" },
    ],
  },
  {
    id: "s4",
    name: "Believer",
    artist: "Imagine Dragons",
    genre: "Rock",
    year: 2017,
    rights: {
      masters: "KIDinaKORNER / Interscope",
      publishing: "Universal Music Publishing",
      lyricists: ["Dan Reynolds", "Wayne Sermon"],
    },
    usage: { allowance: "20% used", commercial: "Allowed", promotional: "Allowed" },
    versions: [
      { id: "s4-v1", name: "Original Version" },
      { id: "s4-v2", name: "Live Performance" },
    ],
  },
  {
    id: "s5",
    name: "Havana",
    artist: "Camila Cabello",
    genre: "Latin",
    year: 2017,
    rights: {
      masters: "Epic Records",
      publishing: "Sony Music Publishing",
      lyricists: ["Camila Cabello", "Frank Dukes"],
    },
    usage: { allowance: "48% used", commercial: "Allowed", promotional: "Restricted" },
    versions: [
      { id: "s5-v1", name: "Original Version" },
      { id: "s5-v2", name: "Live Version" },
    ],
  },
  {
    id: "s6",
    name: "Stay",
    artist: "The Kid LAROI & Justin Bieber",
    genre: "Pop",
    year: 2021,
    rights: {
      masters: "Columbia Records",
      publishing: "Sony Music Publishing",
      lyricists: ["Charlton Howard", "Justin Bieber"],
    },
    usage: { allowance: "15% used", commercial: "Allowed", promotional: "Allowed" },
    versions: [
      { id: "s6-v1", name: "Original Version" },
      { id: "s6-v2", name: "Instrumental" },
    ],
  },
];

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export default function Home() {
  const [activeNav, setActiveNav] = useState("overview");
  const [globalSearch, setGlobalSearch] = useState("");

  const [showcaseOrder, setShowcaseOrder] = useState(null); // null=random, "asc", "desc"
  const [showcaseSongs, setShowcaseSongs] = useState(SONGS);
  const [showcaseIndex, setShowcaseIndex] = useState(0);
  const [slideDir, setSlideDir] = useState("next");
  const [slideKey, setSlideKey] = useState(0);

  // Shuffle client-side only, after mount, to avoid server/client mismatch.
  useEffect(() => {
    setShowcaseSongs(shuffle(SONGS));
  }, []);

  function setOrder(order) {
    setShowcaseOrder(order);
    const sorted = [...SONGS].sort((a, b) =>
      order === "asc"
        ? a.name.localeCompare(b.name)
        : b.name.localeCompare(a.name)
    );
    setShowcaseSongs(sorted);
    setShowcaseIndex(0);
    setSlideDir("next");
    setSlideKey((k) => k + 1);
  }

  function showcaseNext() {
    setSlideDir("next");
    setShowcaseIndex((i) => (i + 1) % showcaseSongs.length);
    setSlideKey((k) => k + 1);
  }

  function showcasePrev() {
    setSlideDir("prev");
    setShowcaseIndex(
      (i) => (i - 1 + showcaseSongs.length) % showcaseSongs.length
    );
    setSlideKey((k) => k + 1);
  }

  const showcaseSong = showcaseSongs[showcaseIndex];

  const stats = useMemo(() => {
    const genres = new Set(SONGS.map((s) => s.genre));
    const artists = new Set(SONGS.map((s) => s.artist));
    const versions = SONGS.reduce((sum, s) => sum + s.versions.length, 0);
    return {
      totalSongs: SONGS.length,
      totalGenres: genres.size,
      totalArtists: artists.size,
      totalVersions: versions,
    };
  }, []);

  const [dashboardSearch, setDashboardSearch] = useState("");
  const [dashboardPick, setDashboardPick] = useState(null);
  const [likedSongs, setLikedSongs] = useState(new Set());
  const [openMenu, setOpenMenu] = useState(null); // id of song/variant menu open
  const [variantPopup, setVariantPopup] = useState(null); // { songId, versionId }
  const [songPopupId, setSongPopupId] = useState(null);

  const [playlists, setPlaylists] = useState([]); // { id, name, songIds: [] }
  const [addToPlaylistFor, setAddToPlaylistFor] = useState(null); // item id
  const [playlistTabName, setPlaylistTabName] = useState("");

  function openAddToPlaylist(itemId) {
    setAddToPlaylistFor(itemId);
    setOpenMenu(null);
  }

  function addToExistingPlaylist(playlistId) {
    setPlaylists((prev) =>
      prev.map((p) =>
        p.id === playlistId
          ? {
              ...p,
              songIds: p.songIds.includes(addToPlaylistFor)
                ? p.songIds
                : [...p.songIds, addToPlaylistFor],
            }
          : p
      )
    );
    setAddToPlaylistFor(null);
  }

  function createPlaylist(name, itemId) {
    if (!name.trim()) return;
    const id = "pl_" + Date.now();
    setPlaylists((prev) => [
      ...prev,
      { id, name: name.trim(), songIds: itemId ? [itemId] : [] },
    ]);
  }

  function getItemMeta(id) {
    const song = SONGS.find((s) => s.id === id);
    if (song) return { title: song.name, subtitle: song.artist, songId: song.id };
    for (const s of SONGS) {
      const v = s.versions.find((v) => v.id === id);
      if (v) return { title: v.name, subtitle: `${s.name} · Variant`, songId: s.id, versionId: v.id };
    }
    return { title: "Unknown", subtitle: "" };
  }

  function openItemPopup(id) {
    const meta = getItemMeta(id);
    if (meta.versionId) {
      setVariantPopup({ songId: meta.songId, versionId: meta.versionId });
    } else {
      setSongPopupId(id);
    }
  }

  const [collapsedGenres, setCollapsedGenres] = useState(new Set());
  const [viewAllGenres, setViewAllGenres] = useState(new Set());
  const [genreSearch, setGenreSearch] = useState({});

  const songsByGenre = useMemo(() => {
    const map = {};
    SONGS.forEach((s) => {
      if (!map[s.genre]) map[s.genre] = [];
      map[s.genre].push(s);
    });
    return map;
  }, []);

  const [collapsedYears, setCollapsedYears] = useState(new Set());
  const [viewAllYears, setViewAllYears] = useState(new Set());
  const [yearSearch, setYearSearch] = useState({});

  const years = useMemo(
    () => [...new Set(SONGS.map((s) => s.year))].sort((a, b) => b - a),
    []
  );

  const songsByYear = useMemo(() => {
    const map = {};
    SONGS.forEach((s) => {
      if (!map[s.year]) map[s.year] = [];
      map[s.year].push(s);
    });
    return map;
  }, []);

  function toggleYearCollapse(year) {
    setCollapsedYears((prev) => {
      const next = new Set(prev);
      next.has(year) ? next.delete(year) : next.add(year);
      return next;
    });
  }

  function toggleViewAllYear(year) {
    setViewAllYears((prev) => {
      const next = new Set(prev);
      next.has(year) ? next.delete(year) : next.add(year);
      return next;
    });
  }

  function jumpToYear(year) {
    document
      .getElementById(`year-${year}`)
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function toggleGenreCollapse(genre) {
    setCollapsedGenres((prev) => {
      const next = new Set(prev);
      next.has(genre) ? next.delete(genre) : next.add(genre);
      return next;
    });
  }

  function toggleViewAll(genre) {
    setViewAllGenres((prev) => {
      const next = new Set(prev);
      next.has(genre) ? next.delete(genre) : next.add(genre);
      return next;
    });
  }

  function toggleLike(id) {
    setLikedSongs((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  function toggleMenu(id) {
    setOpenMenu((prev) => (prev === id ? null : id));
  }

  const dashboardResults = useMemo(() => {
    const q = dashboardSearch.trim().toLowerCase();
    if (!q) return [];
    return SONGS.filter(
      (s) =>
        s.name.toLowerCase().includes(q) || s.artist.toLowerCase().includes(q)
    );
  }, [dashboardSearch]);

  return (
    <div className="shell">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-icon">
            <ShieldCheck size={20} />
          </div>
          <div>
            <div className="brand-name">Music Rights Library</div>
          </div>
        </div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={
                  activeNav === item.id ? "nav-item active" : "nav-item"
                }
                onClick={() => setActiveNav(item.id)}
              >
                <Icon size={17} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-spacer" />

        <button
          className="create-playlist-btn"
          onClick={() => setActiveNav("playlist")}
        >
          <Plus size={16} />
          <span>Create Playlist</span>
        </button>
      </aside>

      {/* MAIN */}
      <div className="shell-main">
        <header className="global-controls">
          <div className="global-search">
            <Search size={16} />
            <input
              value={globalSearch}
              onChange={(e) => setGlobalSearch(e.target.value)}
              placeholder="Search songs, artists..."
            />
          </div>

          <div className="global-controls-right">
            <button
              className={
                showcaseOrder === "asc" ? "icon-btn active" : "icon-btn"
              }
              title="Showcase: Ascending"
              onClick={() => setOrder("asc")}
            >
              <ArrowUpNarrowWide size={16} />
            </button>
            <button
              className={
                showcaseOrder === "desc" ? "icon-btn active" : "icon-btn"
              }
              title="Showcase: Descending"
              onClick={() => setOrder("desc")}
            >
              <ArrowDownNarrowWide size={16} />
            </button>
            <button className="icon-btn" title="Filter">
              <SlidersHorizontal size={16} />
            </button>
          </div>
        </header>

        <main className="shell-content">
          {activeNav === "overview" && (
            <div className="overview-panel">
              <section className="showcase-card">
                <div className="showcase-slide" key={slideKey} data-dir={slideDir}>
                  <div className="showcase-art">
                    <Music2 size={40} />
                  </div>
                  <div className="showcase-info">
                    <div className="showcase-name">{showcaseSong.name}</div>
                    <div className="showcase-artist">{showcaseSong.artist}</div>
                  </div>
                </div>

                <div className="showcase-controls">
                  <button
                    className="showcase-nav-btn"
                    onClick={showcasePrev}
                    aria-label="Previous"
                  >
                    <ChevronLeft size={18} />
                  </button>
                  <button
                    className="showcase-nav-btn"
                    onClick={showcaseNext}
                    aria-label="Next"
                  >
                    <ChevronRight size={18} />
                  </button>
                </div>
              </section>

              <div className="dashboard-grid">
                <MetricCard
                  icon={<Disc3 size={19} />}
                  value={stats.totalSongs}
                  label="Total Songs"
                />
                <MetricCard
                  icon={<Tags size={19} />}
                  value={stats.totalGenres}
                  label="Total Genres"
                />
                <MetricCard
                  icon={<UserRound size={19} />}
                  value={stats.totalArtists}
                  label="Total Artists"
                />
                <MetricCard
                  icon={<FileCheck2 size={19} />}
                  value={stats.totalVersions}
                  label="Total Versions"
                />
              </div>

              <div className="dashboard-search-box">
                <Search size={16} />
                <input
                  value={dashboardSearch}
                  onChange={(e) => {
                    setDashboardSearch(e.target.value);
                    setDashboardPick(null);
                  }}
                  placeholder="Search the library..."
                />
              </div>

              {dashboardSearch.trim() && (
                <div className="dashboard-results">
                  {dashboardResults.length === 0 && (
                    <div className="empty-state">
                      <Search size={22} />
                      <p>No songs found</p>
                    </div>
                  )}

                  {dashboardResults.map((song) => (
                    <button
                      key={song.id}
                      className="dashboard-result-item"
                      onClick={() => setDashboardPick(song.id)}
                    >
                      <div className="result-art">
                        <Music2 size={18} />
                      </div>
                      <div className="result-info">
                        <strong>{song.name}</strong>
                        <span>{song.genre} · {song.year}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {dashboardPick && (
                <SongDetail
                  song={SONGS.find((s) => s.id === dashboardPick)}
                  liked={likedSongs.has(dashboardPick)}
                  onToggleLike={() => toggleLike(dashboardPick)}
                  menuOpen={openMenu === dashboardPick}
                  onToggleMenu={() => toggleMenu(dashboardPick)}
                  onAddToPlaylist={openAddToPlaylist}
                  onOpenVariant={(versionId) =>
                    setVariantPopup({ songId: dashboardPick, versionId })
                  }
                  onOpenRecommended={(id) => setSongPopupId(id)}
                />
              )}

              <div className="subsection-title recently-added-title">
                <CalendarDays size={17} />
                Recently Added
              </div>

              <div className="timeline-scroller">
                {years.map((year) => (
                  <button
                    key={year}
                    className="timeline-year"
                    onClick={() => jumpToYear(year)}
                  >
                    {year}
                  </button>
                ))}
              </div>

              <div className="all-songs-panel">
                {years.map((year) => {
                  const list = songsByYear[year];
                  const collapsed = collapsedYears.has(year);
                  const viewAll = viewAllYears.has(year);
                  const search = yearSearch[year] || "";

                  const visible = viewAll
                    ? list.filter((s) =>
                        s.name.toLowerCase().includes(search.toLowerCase())
                      )
                    : list.slice(0, 5);

                  return (
                    <section
                      className="genre-section"
                      key={year}
                      id={`year-${year}`}
                    >
                      <button
                        className="genre-header"
                        onClick={() => toggleYearCollapse(year)}
                      >
                        <span className="genre-header-title">{year}</span>
                        <span className="genre-header-count">
                          {list.length}
                        </span>
                        <ChevronRight
                          size={16}
                          className={
                            collapsed ? "genre-chevron" : "genre-chevron open"
                          }
                        />
                      </button>

                      {!collapsed && (
                        <>
                          {viewAll && (
                            <div className="dashboard-search-box genre-search-box">
                              <Search size={15} />
                              <input
                                value={search}
                                onChange={(e) =>
                                  setYearSearch((prev) => ({
                                    ...prev,
                                    [year]: e.target.value,
                                  }))
                                }
                                placeholder={`Search in ${year}...`}
                              />
                            </div>
                          )}

                          <div className="song-grid">
                            {visible.map((song) => (
                              <button
                                key={song.id}
                                className="song-card"
                                onClick={() => setSongPopupId(song.id)}
                              >
                                <div className="song-card-art">
                                  <Music2 size={20} />
                                </div>
                                <strong>{song.name}</strong>
                              </button>
                            ))}

                            {viewAll && visible.length === 0 && (
                              <div className="empty-state">
                                <Search size={20} />
                                <p>No songs found</p>
                              </div>
                            )}
                          </div>

                          <button
                            className="view-all-btn"
                            onClick={() => toggleViewAllYear(year)}
                          >
                            {viewAll ? "Show Less" : "View All"}
                          </button>
                        </>
                      )}
                    </section>
                  );
                })}
              </div>

              <div className="subsection-title recommend-title">
                <Music2 size={17} />
                Recommended For You
              </div>

              <div className="song-grid">
                {SONGS.slice()
                  .sort((a, b) => b.year - a.year)
                  .slice(0, 4)
                  .map((song) => (
                    <button
                      key={song.id}
                      className="song-card"
                      onClick={() => setSongPopupId(song.id)}
                    >
                      <div className="song-card-art">
                        <Music2 size={20} />
                      </div>
                      <strong>{song.name}</strong>
                    </button>
                  ))}
              </div>
            </div>
          )}
          {activeNav === "all-songs" && (
            <div className="all-songs-panel">
              {Object.keys(songsByGenre).map((genre) => {
                const list = songsByGenre[genre];
                const collapsed = collapsedGenres.has(genre);
                const viewAll = viewAllGenres.has(genre);
                const search = genreSearch[genre] || "";

                const visible = viewAll
                  ? list.filter((s) =>
                      s.name.toLowerCase().includes(search.toLowerCase())
                    )
                  : list.slice(0, 5);

                return (
                  <section className="genre-section" key={genre}>
                    <button
                      className="genre-header"
                      onClick={() => toggleGenreCollapse(genre)}
                    >
                      <span className="genre-header-title">{genre}</span>
                      <span className="genre-header-count">
                        {list.length}
                      </span>
                      <ChevronRight
                        size={16}
                        className={collapsed ? "genre-chevron" : "genre-chevron open"}
                      />
                    </button>

                    {!collapsed && (
                      <>
                        {viewAll && (
                          <div className="dashboard-search-box genre-search-box">
                            <Search size={15} />
                            <input
                              value={search}
                              onChange={(e) =>
                                setGenreSearch((prev) => ({
                                  ...prev,
                                  [genre]: e.target.value,
                                }))
                              }
                              placeholder={`Search in ${genre}...`}
                            />
                          </div>
                        )}

                        <div className="song-grid">
                          {visible.map((song) => (
                            <button
                              key={song.id}
                              className="song-card"
                              onClick={() => setSongPopupId(song.id)}
                            >
                              <div className="song-card-art">
                                <Music2 size={20} />
                              </div>
                              <strong>{song.name}</strong>
                            </button>
                          ))}

                          {viewAll && visible.length === 0 && (
                            <div className="empty-state">
                              <Search size={20} />
                              <p>No songs found</p>
                            </div>
                          )}
                        </div>

                        <button
                          className="view-all-btn"
                          onClick={() => toggleViewAll(genre)}
                        >
                          {viewAll ? "Show Less" : "View All"}
                        </button>
                      </>
                    )}
                  </section>
                );
              })}
            </div>
          )}

          {activeNav === "liked" && (
            <div className="all-songs-panel">
              {likedSongs.size === 0 ? (
                <div className="placeholder-panel">
                  <Heart size={26} />
                  <h3>No liked songs yet</h3>
                  <p>Tap the heart on any song to add it here.</p>
                </div>
              ) : (
                <section className="genre-section">
                  <div className="genre-header">
                    <span className="genre-header-title">Liked Songs</span>
                    <span className="genre-header-count">
                      {likedSongs.size}
                    </span>
                  </div>

                  <div className="song-grid">
                    {[...likedSongs].map((id) => {
                      const meta = getItemMeta(id);
                      return (
                        <button
                          key={id}
                          className="song-card"
                          onClick={() => openItemPopup(id)}
                        >
                          <div className="song-card-art">
                            <Music2 size={20} />
                          </div>
                          <strong>{meta.title}</strong>
                        </button>
                      );
                    })}
                  </div>
                </section>
              )}
            </div>
          )}

          {activeNav === "playlist" && (
            <div className="all-songs-panel">
              <section className="genre-section">
                <div className="genre-header">
                  <span className="genre-header-title">Create Playlist</span>
                </div>

                <div className="picker-create playlist-tab-create">
                  <input
                    value={playlistTabName}
                    onChange={(e) => setPlaylistTabName(e.target.value)}
                    placeholder="Playlist name..."
                  />
                  <button
                    className="run-button picker-create-btn"
                    disabled={!playlistTabName.trim()}
                    onClick={() => {
                      createPlaylist(playlistTabName, null);
                      setPlaylistTabName("");
                    }}
                  >
                    <Plus size={15} />
                    Create
                  </button>
                </div>
              </section>

              {playlists.length === 0 ? (
                <div className="placeholder-panel">
                  <ListMusic size={26} />
                  <h3>No playlists yet</h3>
                  <p>Create one above, or add a song via its More Options menu.</p>
                </div>
              ) : (
                playlists.map((pl) => (
                  <section className="genre-section" key={pl.id}>
                    <div className="genre-header">
                      <span className="genre-header-title">{pl.name}</span>
                      <span className="genre-header-count">
                        {pl.songIds.length}
                      </span>
                    </div>

                    {pl.songIds.length === 0 ? (
                      <p className="playlist-empty-note">No songs added yet.</p>
                    ) : (
                      <div className="song-grid">
                        {pl.songIds.map((id) => {
                          const meta = getItemMeta(id);
                          return (
                            <button
                              key={id}
                              className="song-card"
                              onClick={() => openItemPopup(id)}
                            >
                              <div className="song-card-art">
                                <Music2 size={20} />
                              </div>
                              <strong>{meta.title}</strong>
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </section>
                ))
              )}
            </div>
          )}
        </main>
      </div>

      {songPopupId && (
        <SongPopup
          song={SONGS.find((s) => s.id === songPopupId)}
          liked={likedSongs.has(songPopupId)}
          onToggleLike={() => toggleLike(songPopupId)}
          menuOpen={openMenu === songPopupId}
          onToggleMenu={() => toggleMenu(songPopupId)}
          onAddToPlaylist={openAddToPlaylist}
          onClose={() => setSongPopupId(null)}
        />
      )}

      {variantPopup && (
        <VariantPopup
          song={SONGS.find((s) => s.id === variantPopup.songId)}
          versionId={variantPopup.versionId}
          liked={likedSongs.has(variantPopup.versionId)}
          onToggleLike={() => toggleLike(variantPopup.versionId)}
          menuOpen={openMenu === variantPopup.versionId}
          onToggleMenu={() => toggleMenu(variantPopup.versionId)}
          onAddToPlaylist={openAddToPlaylist}
          onClose={() => setVariantPopup(null)}
        />
      )}

      {addToPlaylistFor && (
        <PlaylistPicker
          playlists={playlists}
          onClose={() => setAddToPlaylistFor(null)}
          onAddExisting={addToExistingPlaylist}
          onCreate={(name) => {
            createPlaylist(name, addToPlaylistFor);
            setAddToPlaylistFor(null);
          }}
        />
      )}
    </div>
  );
}

function MetricCard({ icon, value, label }) {
  return (
    <div className="metric-card">
      <div className="metric-icon">{icon}</div>
      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>
    </div>
  );
}

function MoreMenu({ open, onToggle, itemId, onAddToPlaylist }) {
  return (
    <div className="more-menu-wrap">
      <button className="icon-btn" onClick={onToggle} aria-label="More options">
        <MoreVertical size={16} />
      </button>
      {open && (
        <div className="more-menu">
          <button onClick={() => onAddToPlaylist(itemId)}>
            <ListPlus size={14} />
            Add to playlist
          </button>
          <button onClick={() => onAddToPlaylist(itemId)}>
            <Plus size={14} />
            Create new playlist
          </button>
        </div>
      )}
    </div>
  );
}

function RightBox({ label, value }) {
  let icon = <CheckCircle2 size={17} />;
  if (value === "Restricted") icon = <XCircle size={17} />;
  else if (Array.isArray(value)) icon = <UserRound size={17} />;

  const display = Array.isArray(value) ? value.join(", ") : value;
  const cls =
    value === "Restricted"
      ? "right-value danger-text"
      : "right-value cleared-text";

  return (
    <div className="right-box">
      <div className="right-label">{label}</div>
      <div className={cls}>
        {icon}
        {display}
      </div>
    </div>
  );
}

function SongDetail({
  song,
  liked,
  onToggleLike,
  menuOpen,
  onToggleMenu,
  onAddToPlaylist,
  onOpenVariant,
  onOpenRecommended,
}) {
  if (!song) return null;

  return (
    <section className="card song-detail" id="track-details">
      <div className="card-header">
        <div>
          <div className="section-kicker">SONG</div>
          <h2>Song Details</h2>
        </div>
        <span className="track-id">{song.id}</span>
      </div>

      <div className="track-main">
        <div className="large-art">
          <Music2 size={42} />
        </div>

        <div className="track-title-area">
          <h3>{song.name}</h3>
          <p>{song.artist}</p>
          <div className="detail-tags">
            <span>{song.genre}</span>
            <span>{song.year}</span>
          </div>
        </div>

        <div className="track-facts">
          <button
            className={liked ? "like-btn liked" : "like-btn"}
            onClick={onToggleLike}
          >
            <HeartIcon size={16} />
            {liked ? "Liked" : "Like"}
          </button>

          <MoreMenu
            open={menuOpen}
            onToggle={onToggleMenu}
            itemId={song.id}
            onAddToPlaylist={onAddToPlaylist}
          />
        </div>
      </div>

      <div className="subsection-title rights-title">
        <LockKeyhole size={17} />
        Rights
      </div>

      <div className="rights-grid">
        <RightBox label="Masters" value={song.rights.masters} />
        <RightBox label="Publishing" value={song.rights.publishing} />
        <RightBox label="Lyricists" value={song.rights.lyricists} />
      </div>

      <div className="subsection-title">
        <ShieldCheck size={17} />
        Usage Information
      </div>

      <div className="rights-grid">
        <RightBox label="Allowance Used" value={song.usage.allowance} />
        <RightBox label="Commercial Usage" value={song.usage.commercial} />
        <RightBox label="Promotional Usage" value={song.usage.promotional} />
      </div>

      <div className="subsection-title">
        <Music2 size={17} />
        Variants
      </div>

      <div className="variant-grid">
        {song.versions.map((v) => (
          <button
            key={v.id}
            className="variant-item"
            onClick={() => onOpenVariant(v.id)}
          >
            <div className="result-art">
              <Music2 size={16} />
            </div>
            <strong>{v.name}</strong>
          </button>
        ))}
      </div>

      <div className="subsection-title">
        <Music2 size={17} />
        Recommended Songs
      </div>

      <div className="song-grid">
        {SONGS.filter((s) => s.id !== song.id)
          .sort((a, b) =>
            a.genre === song.genre && b.genre !== song.genre
              ? -1
              : b.genre === song.genre && a.genre !== song.genre
              ? 1
              : 0
          )
          .slice(0, 4)
          .map((rec) => (
            <button
              key={rec.id}
              className="song-card"
              onClick={() => onOpenRecommended(rec.id)}
            >
              <div className="song-card-art">
                <Music2 size={20} />
              </div>
              <strong>{rec.name}</strong>
            </button>
          ))}
      </div>
    </section>
  );
}

function SongPopup({
  song,
  liked,
  onToggleLike,
  menuOpen,
  onToggleMenu,
  onAddToPlaylist,
  onClose,
}) {
  if (!song) return null;

  return (
    <div className="popup-backdrop" onClick={onClose}>
      <div className="popup-card" onClick={(e) => e.stopPropagation()}>
        <button className="popup-close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>

        <div className="popup-art">
          <Music2 size={30} />
        </div>

        <h3>{song.name}</h3>
        <p>{song.artist}</p>

        <div className="popup-actions">
          <button
            className={liked ? "like-btn liked" : "like-btn"}
            onClick={onToggleLike}
          >
            <HeartIcon size={16} />
            {liked ? "Liked" : "Like"}
          </button>

          <MoreMenu
            open={menuOpen}
            onToggle={onToggleMenu}
            itemId={song.id}
            onAddToPlaylist={onAddToPlaylist}
          />
        </div>
      </div>
    </div>
  );
}

function VariantPopup({
  song,
  versionId,
  liked,
  onToggleLike,
  menuOpen,
  onToggleMenu,
  onAddToPlaylist,
  onClose,
}) {
  if (!song) return null;
  const version = song.versions.find((v) => v.id === versionId);
  if (!version) return null;

  return (
    <div className="popup-backdrop" onClick={onClose}>
      <div className="popup-card" onClick={(e) => e.stopPropagation()}>
        <button className="popup-close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>

        <div className="popup-art">
          <Music2 size={30} />
        </div>

        <h3>{version.name}</h3>
        <p>{song.name} · {song.artist}</p>

        <div className="popup-actions">
          <button
            className={liked ? "like-btn liked" : "like-btn"}
            onClick={onToggleLike}
          >
            <HeartIcon size={16} />
            {liked ? "Liked" : "Like"}
          </button>

          <MoreMenu
            open={menuOpen}
            onToggle={onToggleMenu}
            itemId={version.id}
            onAddToPlaylist={onAddToPlaylist}
          />
        </div>
      </div>
    </div>
  );
}

function PlaylistPicker({ playlists, onClose, onAddExisting, onCreate }) {
  const [name, setName] = useState("");

  return (
    <div className="popup-backdrop" onClick={onClose}>
      <div className="popup-card picker-card" onClick={(e) => e.stopPropagation()}>
        <button className="popup-close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>

        <h3>Add to Playlist</h3>

        {playlists.length > 0 && (
          <div className="picker-list">
            {playlists.map((p) => (
              <button
                key={p.id}
                className="picker-list-item"
                onClick={() => onAddExisting(p.id)}
              >
                <ListMusic size={15} />
                <span>{p.name}</span>
                <span className="picker-count">{p.songIds.length}</span>
              </button>
            ))}
          </div>
        )}

        <div className="picker-create">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="New playlist name..."
          />
          <button
            className="run-button picker-create-btn"
            disabled={!name.trim()}
            onClick={() => onCreate(name)}
          >
            <Plus size={15} />
            Create
          </button>
        </div>
      </div>
    </div>
  );
}