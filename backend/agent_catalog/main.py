from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SyncRights Catalog Agent")


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search_tracks(q: str = ""):
    # TODO (Day 8):
    # Replace this hardcoded response with real search
    # against the catalog seed/merged data.

    return [
        {
            "track_id": "trk_001",
            "title": "Velvet Comet",
            "artist": "Nora Venn",
            "aliases": [
                "Velvet Comet",
                "Velvet Comet Song"
            ],
            "genre": [
                "indie pop",
                "electronic"
            ],
            "release_year": 2016,
            "versions": [
                "ver_001_a",
                "ver_001_b",
                "ver_001_c"
            ]
        }
    ]