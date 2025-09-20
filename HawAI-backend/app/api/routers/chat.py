from fastapi import APIRouter, HTTPException, Request
from app.schemas.chat import ChatIn, ChatOut, Source, Safety
from app.services.ollama_client import OllamaClient
from app.services.sdg_classifier import classify_sdg_tags
from app.services.postprocess import apply_emergency_if_needed, build_sources
from app.core.rate_limit import limiter
from app.core.config import settings

router = APIRouter()


@router.post("/chat", response_model=ChatOut)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, body: ChatIn) -> ChatOut:
    async with OllamaClient() as client:
        try:
            reply_text = await client.generate(body.message, body.user_meta)
        except Exception as e:  # pragma: no cover
            raise HTTPException(status_code=502, detail=f"Ollama upstream error: {e}")

    tagged = classify_sdg_tags(body.message + "\n" + reply_text)
    reply_text, is_emergency = apply_emergency_if_needed(body.message, reply_text)
    sources = [Source(**s) for s in build_sources()]

    return ChatOut(
        reply=reply_text,
        sdg_tags=tagged,
        sources=sources,
        safety=Safety(is_emergency=is_emergency),
    )
