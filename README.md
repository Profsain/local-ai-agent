# Local AI Agent

A practical local AI agent using Python, FastAPI, Ollama/Llama 3.2, SQLite memory, and tool calling.

## Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.2:3b
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and try:
- What is 27 * 19?
- What time is it?
- Explain RAG to a beginner.
- What did I ask you earlier?

## Architecture
Browser -> FastAPI -> Agent -> Ollama
                         |-> calculator
                         |-> current_time
                         |-> SQLite conversation history
