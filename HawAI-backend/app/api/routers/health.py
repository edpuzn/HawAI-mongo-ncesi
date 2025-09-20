from fastapi import APIRouter
from app.core.config import settings
from app.services.ollama_client import OllamaClient

router = APIRouter()


@router.get("/healthz")
async def healthz():
    reachable = False
    try:
        async with OllamaClient() as oc:
            reachable = await oc.ping()
    except Exception:
        reachable = False
    return {
        "status": "ok",
        "ollama": {
            "reachable": reachable,
            "host": settings.ollama_host,
        },
    }
