"use client";

import { useMemo, useState } from "react";

import {
  Search,
  Music2,
  ShieldCheck,
  AlertTriangle,
  XCircle,
  CheckCircle2,
  ChevronRight,
  Play,
  Clock3,
  UserRound,
  CalendarDays,
  Database,
  Activity,
  ExternalLink,
  Send,
  FileCheck2,
  LockKeyhole,
  CircleHelp,
  BarChart3,
} from "lucide-react";

const tracks = [
  {
    id: "trk_001",
    title: "Blinding Lights",
    artist: "The Weeknd",
    genre: ["pop", "synthwave"],
    releaseYear: 2019,
    duration: "3:20",
    versions: [
      {
        id: "ver_001_original",
        name: "Original Version",
        type: "Original",
        duration: "3:20",
        status: "Cleared",
      },
      {
        id: "ver_001_live",
        name: "Live Version",
        type: "Live",
        duration: "3:42",
        status: "Review Required",
      },
      {
        id: "ver_001_instrumental",
        name: "Instrumental",
        type: "Instrumental",
        duration: "3:20",
        status: "Cleared",
      },
    ],
    rights: {
      master: "Cleared",
      publishing: "Cleared",
      sync: "Conditional",
      territory: "Worldwide",
    },
  },

  {
    id: "trk_002",
    title: "Levitating",
    artist: "Dua Lipa",
    genre: ["pop", "dance"],
    releaseYear: 2020,
    duration: "3:23",
    versions: [
      {
        id: "ver_002_original",
        name: "Album Version",
        type: "Original",
        duration: "3:23",
        status: "Cleared",
      },
      {
        id: "ver_002_remix",
        name: "Remix Version",
        type: "Remix",
        duration: "3:57",
        status: "Review Required",
      },
    ],
    rights: {
      master: "Cleared",
      publishing: "Cleared",
      sync: "Cleared",
      territory: "Worldwide",
    },
  },

  {
    id: "trk_003",
    title: "Shape of You",
    artist: "Ed Sheeran",
    genre: ["pop"],
    releaseYear: 2017,
    duration: "3:53",
    versions: [
      {
        id: "ver_003_original",
        name: "Original Version",
        type: "Original",
        duration: "3:53",
        status: "Cleared",
      },
      {
        id: "ver_003_acoustic",
        name: "Acoustic Version",
        type: "Acoustic",
        duration: "3:46",
        status: "Restricted",
      },
    ],
    rights: {
      master: "Cleared",
      publishing: "Conditional",
      sync: "Restricted",
      territory: "Selected Territories",
    },
  },

  {
    id: "trk_004",
    title: "Believer",
    artist: "Imagine Dragons",
    genre: ["rock", "alternative"],
    releaseYear: 2017,
    duration: "3:24",
    versions: [
      {
        id: "ver_004_original",
        name: "Original Version",
        type: "Original",
        duration: "3:24",
        status: "Cleared",
      },
      {
        id: "ver_004_live",
        name: "Live Performance",
        type: "Live",
        duration: "4:01",
        status: "Cleared",
      },
    ],
    rights: {
      master: "Cleared",
      publishing: "Cleared",
      sync: "Cleared",
      territory: "Worldwide",
    },
  },

  {
    id: "trk_005",
    title: "Havana",
    artist: "Camila Cabello",
    genre: ["pop", "latin"],
    releaseYear: 2017,
    duration: "3:37",
    versions: [
      {
        id: "ver_005_original",
        name: "Original Version",
        type: "Original",
        duration: "3:37",
        status: "Cleared",
      },
      {
        id: "ver_005_live",
        name: "Live Version",
        type: "Live",
        duration: "3:55",
        status: "Review Required",
      },
    ],
    rights: {
      master: "Cleared",
      publishing: "Conditional",
      sync: "Conditional",
      territory: "Worldwide",
    },
  },

  {
    id: "trk_006",
    title: "Stay",
    artist: "The Kid LAROI & Justin Bieber",
    genre: ["pop"],
    releaseYear: 2021,
    duration: "2:21",
    versions: [
      {
        id: "ver_006_original",
        name: "Original Version",
        type: "Original",
        duration: "2:21",
        status: "Cleared",
      },
      {
        id: "ver_006_instrumental",
        name: "Instrumental",
        type: "Instrumental",
        duration: "2:21",
        status: "Cleared",
      },
    ],
    rights: {
      master: "Cleared",
      publishing: "Cleared",
      sync: "Cleared",
      territory: "Worldwide",
    },
  },
];

const sampleQueries = [
  "Can I use this track in a YouTube advertisement?",
  "Can I use this song in a commercial campaign?",
  "Is this track cleared for worldwide social media use?",
];

export default function Home() {
  const [search, setSearch] = useState("");
  const [selectedTrackId, setSelectedTrackId] = useState("trk_001");
  const [query, setQuery] = useState("");
  const [verdict, setVerdict] = useState(null);
  const [activeGenre, setActiveGenre] = useState("All");

  const selectedTrack =
    tracks.find((track) => track.id === selectedTrackId) || tracks[0];

  const genres = useMemo(() => {
    const values = tracks.flatMap((track) => track.genre);
    return ["All", ...new Set(values)];
  }, []);

  const filteredTracks = useMemo(() => {
    return tracks.filter((track) => {
      const matchesSearch =
        track.title.toLowerCase().includes(search.toLowerCase()) ||
        track.artist.toLowerCase().includes(search.toLowerCase());

      const matchesGenre =
        activeGenre === "All" || track.genre.includes(activeGenre);

      return matchesSearch && matchesGenre;
    });
  }, [search, activeGenre]);

  function selectTrack(trackId) {
    setSelectedTrackId(trackId);
    setVerdict(null);

    document
      .getElementById("track-details")
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function runComplianceCheck() {
    if (!query.trim()) return;

    const lower = query.toLowerCase();

    let result;

    if (
      lower.includes("commercial") ||
      lower.includes("advertisement") ||
      lower.includes("youtube")
    ) {
      if (selectedTrack.rights.sync === "Cleared") {
        result = {
          type: "success",
          title: "Usage Allowed",
          description:
            "The selected track appears eligible for this requested use based on the current rights data.",
          score: 96,
        };
      } else if (selectedTrack.rights.sync === "Conditional") {
        result = {
          type: "warning",
          title: "Review Required",
          description:
            "The selected track has conditional synchronization rights. Additional clearance may be required before commercial use.",
          score: 68,
        };
      } else {
        result = {
          type: "danger",
          title: "Usage Restricted",
          description:
            "The selected track is currently restricted for synchronization use. Do not proceed without additional rights clearance.",
          score: 24,
        };
      }
    } else {
      result = {
        type: "warning",
        title: "Manual Review Recommended",
        description:
          "The query requires additional context. The system recommends reviewing the applicable master, publishing and synchronization rights.",
        score: 72,
      };
    }

    setVerdict(result);

    setTimeout(() => {
      document
        .getElementById("verdict")
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 50);
  }

  return (
    <main className="app-shell">
      {/* TOP NAV */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">
            <ShieldCheck size={23} />
          </div>

          <div>
            <div className="brand-name">SyncRights</div>
            <div className="brand-subtitle">
              Music Rights Intelligence
            </div>
          </div>
        </div>

        <div className="system-status">
          <span className="status-dot" />
          System Operational
        </div>
      </header>

      {/* HERO */}
      <section className="hero">
        <div>
          <div className="eyebrow">
            <Database size={15} />
            RIGHTS & COMPLIANCE PLATFORM
          </div>

          <h1>
            Music rights.
            <br />
            <span>Made searchable.</span>
          </h1>

          <p>
            Search your music catalog, inspect rights, and instantly evaluate
            compliance questions from one unified workspace.
          </p>
        </div>

        <div className="hero-stat">
          <div className="hero-stat-icon">
            <Activity size={20} />
          </div>

          <div>
            <strong>{tracks.length}</strong>
            <span>Catalog Tracks</span>
          </div>
        </div>
      </section>

      {/* MAIN WORKSPACE */}
      <section className="workspace">
        {/* P1 */}
        <aside className="library-panel">
          <div className="section-heading">
            <div>
              <div className="section-kicker">P1</div>
              <h2>Music Library</h2>
            </div>

            <div className="count-pill">{filteredTracks.length}</div>
          </div>

          <div className="search-box">
            <Search size={18} />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search tracks or artists..."
            />
          </div>

          <div className="genre-list">
            {genres.map((genre) => (
              <button
                key={genre}
                className={
                  activeGenre === genre
                    ? "genre-button active"
                    : "genre-button"
                }
                onClick={() => setActiveGenre(genre)}
              >
                {genre}
              </button>
            ))}
          </div>

          <div className="track-list">
            {filteredTracks.map((track) => (
              <button
                key={track.id}
                className={
                  selectedTrackId === track.id
                    ? "track-item selected"
                    : "track-item"
                }
                onClick={() => selectTrack(track.id)}
              >
                <div className="track-art">
                  <Music2 size={18} />
                </div>

                <div className="track-info">
                  <strong>{track.title}</strong>
                  <span>{track.artist}</span>

                  <div className="track-meta">
                    <span>{track.releaseYear}</span>
                    <span>•</span>
                    <span>{track.versions.length} versions</span>
                  </div>
                </div>

                <ChevronRight size={17} className="track-arrow" />
              </button>
            ))}

            {filteredTracks.length === 0 && (
              <div className="empty-state">
                <Search size={24} />
                <p>No tracks found</p>
              </div>
            )}
          </div>
        </aside>

        {/* RIGHT SIDE */}
        <div className="content-area">
          {/* P2 */}
          <section className="card track-details" id="track-details">
            <div className="card-header">
              <div>
                <div className="section-kicker">P2</div>
                <h2>Track Details</h2>
              </div>

              <span className="track-id">{selectedTrack.id}</span>
            </div>

            <div className="track-main">
              <div className="large-art">
                <Music2 size={42} />
              </div>

              <div className="track-title-area">
                <h3>{selectedTrack.title}</h3>
                <p>{selectedTrack.artist}</p>

                <div className="detail-tags">
                  {selectedTrack.genre.map((genre) => (
                    <span key={genre}>{genre}</span>
                  ))}
                </div>
              </div>

              <div className="track-facts">
                <div>
                  <CalendarDays size={16} />
                  <span>{selectedTrack.releaseYear}</span>
                </div>

                <div>
                  <Clock3 size={16} />
                  <span>{selectedTrack.duration}</span>
                </div>

                <div>
                  <UserRound size={16} />
                  <span>Artist</span>
                </div>
              </div>
            </div>

            <div className="subsection-title">
              <Music2 size={17} />
              Versions
            </div>

            <div className="versions">
              {selectedTrack.versions.map((version) => (
                <div className="version-row" key={version.id}>
                  <div className="version-icon">
                    <Play size={14} />
                  </div>

                  <div className="version-info">
                    <strong>{version.name}</strong>
                    <span>
                      {version.id} · {version.type}
                    </span>
                  </div>

                  <span className="version-duration">
                    {version.duration}
                  </span>

                  <StatusBadge status={version.status} />
                </div>
              ))}
            </div>

            <div className="subsection-title rights-title">
              <LockKeyhole size={17} />
              Rights Summary
            </div>

            <div className="rights-grid">
              <RightBox
                label="Master"
                value={selectedTrack.rights.master}
              />

              <RightBox
                label="Publishing"
                value={selectedTrack.rights.publishing}
              />

              <RightBox
                label="Synchronization"
                value={selectedTrack.rights.sync}
              />

              <RightBox
                label="Territory"
                value={selectedTrack.rights.territory}
              />
            </div>
          </section>

          {/* P3 */}
          <section className="card query-card">
            <div className="card-header">
              <div>
                <div className="section-kicker">P3</div>
                <h2>Compliance Query</h2>
              </div>

              <div className="query-status">
                <CircleHelp size={16} />
                Ask about this track
              </div>
            </div>

            <p className="card-description">
              Describe the intended use of the selected track. The compliance
              engine will evaluate the request against the available rights.
            </p>

            <div className="query-input-wrapper">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Example: Can I use this track in a YouTube advertisement?"
              />

              <button
                className="run-button"
                onClick={runComplianceCheck}
                disabled={!query.trim()}
              >
                <Send size={17} />
                Run Compliance Check
              </button>
            </div>

            <div className="sample-queries">
              <span>Try an example:</span>

              {sampleQueries.map((sample) => (
                <button
                  key={sample}
                  onClick={() => setQuery(sample)}
                >
                  {sample}
                </button>
              ))}
            </div>
          </section>

          {/* P4 */}
          <section className="card verdict-card" id="verdict">
            <div className="card-header">
              <div>
                <div className="section-kicker">P4</div>
                <h2>Compliance Verdict</h2>
              </div>

              <div className="dashboard-link">
                <BarChart3 size={16} />
                Grafana Dashboard
                <ExternalLink size={14} />
              </div>
            </div>

            {!verdict ? (
              <div className="waiting-verdict">
                <div className="waiting-icon">
                  <FileCheck2 size={32} />
                </div>

                <h3>Ready for analysis</h3>

                <p>
                  Submit a compliance question above to generate a verdict
                  for <strong>{selectedTrack.title}</strong>.
                </p>
              </div>
            ) : (
              <VerdictResult verdict={verdict} track={selectedTrack} />
            )}
          </section>

          {/* DASHBOARD SUMMARY */}
          <section className="dashboard-grid">
            <MetricCard
              icon={<Music2 size={19} />}
              value={tracks.length}
              label="Tracks Indexed"
            />

            <MetricCard
              icon={<FileCheck2 size={19} />}
              value={tracks.reduce(
                (total, track) => total + track.versions.length,
                0
              )}
              label="Versions Cataloged"
            />

            <MetricCard
              icon={<ShieldCheck size={19} />}
              value="94.2%"
              label="Rights Coverage"
            />

            <MetricCard
              icon={<Activity size={19} />}
              value="99.9%"
              label="System Uptime"
            />
          </section>
        </div>
      </section>

      <footer className="footer">
        <span>SyncRights</span>
        <span>Music Rights Intelligence Platform</span>
        <span>Frontend Prototype · P1–P4</span>
      </footer>
    </main>
  );
}

function StatusBadge({ status }) {
  let className = "status-badge";

  if (status === "Cleared") {
    className += " cleared";
  } else if (status === "Review Required") {
    className += " review";
  } else {
    className += " restricted";
  }

  return <span className={className}>{status}</span>;
}

function RightBox({ label, value }) {
  let icon = <CheckCircle2 size={17} />;

  if (value === "Conditional") {
    icon = <AlertTriangle size={17} />;
  }

  if (
    value === "Restricted" ||
    value === "Selected Territories"
  ) {
    icon = <XCircle size={17} />;
  }

  return (
    <div className="right-box">
      <div className="right-label">{label}</div>

      <div
        className={
          value === "Cleared"
            ? "right-value cleared-text"
            : value === "Conditional"
            ? "right-value warning-text"
            : "right-value danger-text"
        }
      >
        {icon}
        {value}
      </div>
    </div>
  );
}

function VerdictResult({ verdict, track }) {
  const config = {
    success: {
      icon: <CheckCircle2 size={42} />,
      className: "success",
    },
    warning: {
      icon: <AlertTriangle size={42} />,
      className: "warning",
    },
    danger: {
      icon: <XCircle size={42} />,
      className: "danger",
    },
  };

  const current = config[verdict.type];

  return (
    <div className="verdict-result">
      <div className={`verdict-main ${current.className}`}>
        <div className="verdict-icon">{current.icon}</div>

        <div>
          <div className="verdict-label">FINAL VERDICT</div>
          <h3>{verdict.title}</h3>

          <p>{verdict.description}</p>
        </div>

        <div className="confidence">
          <strong>{verdict.score}%</strong>
          <span>Confidence</span>
        </div>
      </div>

      <div className="analysis-grid">
        <div className="analysis-item">
          <span>Track</span>
          <strong>{track.title}</strong>
        </div>

        <div className="analysis-item">
          <span>Master Rights</span>
          <strong>{track.rights.master}</strong>
        </div>

        <div className="analysis-item">
          <span>Publishing</span>
          <strong>{track.rights.publishing}</strong>
        </div>

        <div className="analysis-item">
          <span>Sync Rights</span>
          <strong>{track.rights.sync}</strong>
        </div>
      </div>

      <div className="verdict-note">
        <ShieldCheck size={18} />

        <span>
          This result is generated from the current catalog and rights
          dataset. Final legal clearance should be confirmed before
          commercial release.
        </span>
      </div>
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