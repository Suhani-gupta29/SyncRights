from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="SyncRights Orchestrator (P3)")

# Ye wo format hai jo frontend se aayega
class UserQuery(BaseModel):
    query: str
    
@app.get("/")
async def root():
    return {"message": "P3 Orchestrator is running and ready for Day 11 Pipeline Wiring!"}    

@app.post("/query")
async def run_full_pipeline(request: UserQuery):
    """
    Day 9 Task: Orchestrator Skeleton.
    This will eventually chain P1 -> P2 -> P3 -> P4.
    """
    user_text = request.query
    
    try:
        # Step 1: P1 (Catalog Search) - Placeholder
        mock_p1_track_id = "trk_001" 
        
        # Step 2: P2 (Version Matcher) - Placeholder
        mock_p2_version_id = "ver_001_c"
        
        # Step 3: P3 (Rights Lookup) - Connecting to Sanket's own logic
        from lookup import get_rights_data
        p3_rights = get_rights_data(mock_p2_version_id)
        
        # Step 4: P4 (Compliance/Recommendation) - Placeholder
        mock_p4_verdict = {
            "type": "success",
            "title": "Usage Allowed",
            "description": "Mocked verdict from P4.",
            "score": 95
        }
        
        # Final combined response going back to the frontend
        return {
            "status": "success",
            "original_query": user_text,
            "track_id": mock_p1_track_id,
            "version_id": mock_p2_version_id,
            "rights_summary": p3_rights,
            "final_verdict": mock_p4_verdict
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Terminal run command: uvicorn orchestrator:app --reload --port 8000