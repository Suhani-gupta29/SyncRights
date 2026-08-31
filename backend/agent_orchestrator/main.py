from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from orchestrator import run_agent

app = FastAPI(title="SyncRights Agent Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# app = FastAPI() ke theek neeche:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Yahan "*" mat lagana!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok", "agent": "orchestrator"}


@app.post("/agent/query")
def query(req: QueryRequest):
    try:
        result = run_agent(req.question)
        return result
    except Exception as e:
        return {
            "error": f"agent_run_failed: {e}",
            "answer": None,
            "trace": [],
        }