import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .agent import LocalAIAgent, AgentError
from .config import OLLAMA_MODEL
from .db import init_db, add_message, get_messages

app = FastAPI(title="Local AI Agent", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
agent = LocalAIAgent()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None
class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.on_event("startup")
def startup(): init_db()
@app.get("/")
def home(): return FileResponse("static/index.html")
@app.get("/health")
def health(): return {"status":"ok", "model":OLLAMA_MODEL}
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    sid = req.session_id or str(uuid.uuid4())
    try: answer = agent.run(get_messages(sid), req.message)
    except AgentError as e: raise HTTPException(status_code=503, detail=str(e))
    add_message(sid,"user",req.message); add_message(sid,"assistant",answer)
    return ChatResponse(session_id=sid,response=answer)
