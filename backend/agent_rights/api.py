from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from lookup import get_rights_data

app = FastAPI(title="P3 Rights Intelligence Agent")

class RightsRequest(BaseModel):
    version_id: str

@app.post("/rights")
async def fetch_rights(request: RightsRequest):
    result = get_rights_data(request.version_id)
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result

# Run command: uvicorn api:app --reload --port 8003