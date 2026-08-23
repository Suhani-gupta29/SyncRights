from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rule_based import router as rule_router
from gemini_based import router as gemini_router

app = FastAPI(title="SyncRights Recommendation Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "agent": "recommendation-standalone"}


app.include_router(rule_router)
app.include_router(gemini_router)