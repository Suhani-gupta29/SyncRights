from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import clickhouse_connect

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from orchestrator import run_agent

app = FastAPI(title="SyncRights Agent Orchestrator")

def get_clickhouse_client():
    try:
        # Yahan apne ClickHouse Cloud ke actual details daal
        client = clickhouse_connect.get_client(
            host='https://w2u7lzcs7w.ap-south-1.aws.clickhouse.cloud', 
            port=8443, 
            username='default', 
            password='L22_NWwBqIL3V',
            secure=True
        )
        
        # Table auto-create command
        client.command('''
            CREATE TABLE IF NOT EXISTS syncrights_events (
                timestamp DateTime DEFAULT now(),
                version_id String,
                license_status String
            ) ENGINE = MergeTree()
            ORDER BY timestamp
        ''')
        
        return client
    except Exception as e:
        print(f"ClickHouse connection failed: {e}")
        return None

def log_p2_version_event(version_id: str, license_status: str):
    client = get_clickhouse_client()
    if client:
        try:
            # Table ka naam 'syncrights_events' assume kar rahe hain
            data = [[version_id, license_status]]
            client.insert('syncrights_events', data, column_names=['version_id', 'license_status'])
            print(f"✅ P2 Data Logged to ClickHouse: Version {version_id} | Status: {license_status}")
        except Exception as e:
            print(f"Error logging to ClickHouse: {e}")

# Yahan maine single, correct CORS block rakha hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok", "agent": "orchestrator"}

# 🚀 YEH THA STEP 2C: Yahan background_tasks add kiya gaya hai
@app.post("/agent/query")
def query(req: QueryRequest, background_tasks: BackgroundTasks):
    try:
        # Agent ne apna dimag lagaya aur result nikala
        result = run_agent(req.question)
        
        # --- Tera P2 Day 13 Task (Logging) ---
        # Abhi test karne ke liye hum dummy data bhej rahe hain. 
        # (Asli version_id baad mein 'result' dictionary se extract kar lenge)
        extracted_version = "ver_001_c" 
        extracted_status = "Active" 
        
        # Ye line API ko bina roke background mein ClickHouse ko data bhej degi
        background_tasks.add_task(log_p2_version_event, extracted_version, extracted_status)
        # -------------------------------------

        return result
    except Exception as e:
        return {
            "error": f"agent_run_failed: {e}",
            "answer": None,
            "trace": [],
        }