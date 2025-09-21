from __future__ import annotations
from fastapi import APIRouter, Header, HTTPException
from typing import Any, Dict, List, Optional
import httpx
from app.core.config import settings
from app.services.ollama_client import OllamaClient
from app.services.postprocess import override_identity_if_needed


router = APIRouter(prefix="/v1")


@router.get("/models")
async def list_models() -> Dict[str, Any]:
    # Query Ollama for available models; fallback to settings.model_name
    models: List[Dict[str, str]] = []
    try:
        async with httpx.AsyncClient(base_url=settings.ollama_host, timeout=5) as ac:
            r = await ac.get("/api/tags")
            if r.status_code == 200:
                names = [m.get("name") for m in r.json().get("models", [])]
                for name in names:
                    if name:
                        models.append({"id": name, "object": "model", "owned_by": "owner"})
    except Exception:
        pass
    if not models:
        models = [{"id": settings.model_name, "object": "model", "owned_by": "owner"}]
    return {"object": "list", "data": models}


@router.post("/chat/completions")
async def chat_completions(
    body: Dict[str, Any],
    authorization: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    # Simple API key guard (optional)
    expected = settings.compat_api_key
    if expected:
        token = None
        if authorization and authorization.lower().startswith("bearer "):
            token = authorization.split(" ", 1)[1]
        if token != expected:
            raise HTTPException(status_code=401, detail="invalid api key")

    messages_in: List[Dict[str, str]] = body.get("messages") or []
    # Inject system message from env if not present (to keep branding)
    if settings.system_prompt and (not messages_in or messages_in[0].get("role") != "system"):
        messages_in = [{"role": "system", "content": settings.system_prompt}] + messages_in
    temperature = float(body.get("temperature", 0.2))
    model = body.get("model") or settings.model_name

    async with OllamaClient(model=model) as client:
        content = await client.chat_messages(messages_in, temperature=temperature)
    # Apply identity override for questions like "Sen kimsin?"
    user_text = next((m.get("content", "") for m in reversed(messages_in) if m.get("role") == "user"), "")
    content = override_identity_if_needed(user_text, content)

    # OpenAI-compatible shape
    return {
        "id": "chatcmpl-xxx",
        "object": "chat.completion",
        "created": 0,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
    }


