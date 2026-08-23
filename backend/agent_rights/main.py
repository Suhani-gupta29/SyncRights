from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint updated to match your README contract
@app.get("/rights/{track_id}/{version_id}")
def lookup_rights(track_id: str, version_id: str):
    # Faked response for Day 6 deployment testing based on rights_p2.json
    return {
        "version_id": version_id,
        "track_id": track_id,
        "master_rights_holder": "Orbit Sound Label",
        "publishing_rights_holder": "Everline Publishing",
        "composer": ["Kaelen Roe"],
        "lyricist": ["Kaelen Roe"],
        "singer": ["Kaelen Roe"],
        "rights_type_held": [
            "master",
            "publishing",
            "composer",
            "lyricist",
            "singer"
        ],
        "usage_types_allowed": [
            "social media campaign",
            "trailer"
        ],
        "license_status": "active",
        "license_start_date": "2018-10-05",
        "license_end_date": "2025-09-01",
        "commercial_use_allowed": True,
        "promotional_use_only": False,
        "previous_usages": [
            "trk_021_gameE_2025"
        ]
    }