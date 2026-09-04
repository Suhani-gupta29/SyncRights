from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import clickhouse_connect
from datetime import datetime

def log_conflict(track_id: str, agent_id: str, reason: str):
    """Logs a detected conflict directly to the shared ClickHouse database."""
    try:
        client = clickhouse_connect.get_client(
            host='w2u7lzcs7w.ap-south-1.aws.clickhouse.cloud', 
            port=8443, 
            username='default', 
            password='L22_NWwBqIL3V',
            secure=True
        )
        
        row = [datetime.now(), 'rights_conflict', track_id, agent_id, reason, 1]
        
        client.insert(
            'events', 
            [row], 
            column_names=['timestamp', 'event_type', 'track_id', 'agent_id', 'conflict_reason', 'has_conflict']
        )
    except Exception as e:
        print(f"ClickHouse logging failed: {e}")
        
app = FastAPI(title="SyncRights Orchestrator (P3)")

class UserQuery(BaseModel):
    query: str
    
@app.get("/")
async def root():
    return {"message": "P3 Orchestrator is running and ready for Day 13 Logging!"}    

@app.post("/query")
async def run_full_pipeline(request: UserQuery):
    user_text = request.query
    
    try:
        # Step 1: P1 (Catalog Search) - Placeholder
        mock_p1_track_id = "trk_001" 
        
        # Step 2: P2 (Version Matcher) - Placeholder
        mock_p2_version_id = "ver_001_c"
        
        # Step 3: P3 (Rights Lookup) - Connecting to your logic
        from lookup import get_rights_data
        p3_rights = get_rights_data(mock_p2_version_id)
        
        # ==========================================
        # DAY 13 TASK: TRIGGER CONFLICT LOG HERE
        # ==========================================
        # This assumes your get_rights_data function returns a dictionary 
        # indicating if a conflict exists. Adjust the keys to match your actual lookup.py logic.
        if p3_rights.get("conflict_detected") == True or p3_rights.get("status") == "conflict":
            reason = p3_rights.get("conflict_reason", "Territory or License Conflict")
            agent = p3_rights.get("agent_id", "AGT-UNKNOWN")
            
            # Fire the event to ClickHouse
            log_conflict(track_id=mock_p1_track_id, agent_id=agent, reason=reason)
        # ==========================================
        
        # Step 4: P4 (Compliance/Recommendation) - Placeholder
        mock_p4_verdict = {
            "type": "success",
            "title": "Usage Allowed",
            "description": "Mocked verdict from P4.",
            "score": 95
        }
        
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