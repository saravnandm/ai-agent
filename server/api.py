import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.db import init_db, clear_user_history
from core.agent import generate_agent_reply

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI setup ---
app = FastAPI(title="AI Agent (Gemini + Tools)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# --- Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- Routes ---
@app.get("/")
def root():
    return {"message": "AI Agent with Gemini + Tools is running"}

@app.post("/chat")
async def chat(req: ChatRequest):
    reply = generate_agent_reply(req.user_id, req.message)
    return {"reply": reply}

@app.post("/clear")
async def clear(req: ChatRequest):
    clear_user_history(req.user_id)
    return {"status": f"cleared for user {req.user_id}"}
