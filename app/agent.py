import json, requests
from .config import OLLAMA_URL, OLLAMA_MODEL, SYSTEM_PROMPT
from .tools import TOOLS, TOOL_DEFINITIONS

class AgentError(Exception): pass

class LocalAIAgent:
    def _ask(self, messages):
        try:
            r = requests.post(OLLAMA_URL, json={"model":OLLAMA_MODEL,"messages":messages,"tools":TOOL_DEFINITIONS,"stream":False,"options":{"temperature":0.2}}, timeout=120)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.ConnectionError as e: raise AgentError("Cannot connect to Ollama. Start Ollama first.") from e
        except requests.exceptions.Timeout as e: raise AgentError("Ollama request timed out.") from e
        except requests.exceptions.RequestException as e: raise AgentError(f"Ollama request failed: {e}") from e

    def run(self, history, user_message):
        messages = [{"role":"system","content":SYSTEM_PROMPT}, *history, {"role":"user","content":user_message}]
        for _ in range(5):
            data = self._ask(messages)
            msg = data.get("message", {})
            calls = msg.get("tool_calls") or []
            if not calls:
                return msg.get("content", "").strip()
            messages.append(msg)
            for call in calls:
                fn = call.get("function", {})
                name, args = fn.get("name"), fn.get("arguments", {})
                if isinstance(args, str): args = json.loads(args)
                tool = TOOLS.get(name)
                result = tool(**args) if tool else f"Unknown tool: {name}"
                messages.append({"role":"tool","content":str(result)})
        raise AgentError("Maximum tool iterations exceeded.")
