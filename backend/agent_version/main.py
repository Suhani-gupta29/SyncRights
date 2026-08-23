from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/version/match")
def identify_version(track_id: str, q: str = ""):
    # Faked response for Day 6 deployment testing
    return {
        "version_id": "ver_021_b",
        "track_id": track_id,
        "display_label": "2023 Remastered Version",
        "version_type": "remaster",
        "featured_artists": []
    }