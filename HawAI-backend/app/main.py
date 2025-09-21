from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.security import get_cors_config
from app.core.rate_limit import RateLimitMiddleware
from app.middlewares.request_id import RequestIDMiddleware
from app.api.routers.health import router as health_router
from app.api.routers.chat import router as chat_router
from app.services.competition import router as competition_router
from app.api.routers.compat import router as compat_router


configure_logging()

app = FastAPI(title="HawAI API", version="0.1.0")

# CORS
cors_conf = get_cors_config(settings)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_conf["allow_origins"],
    allow_credentials=cors_conf["allow_credentials"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Request ID
app.add_middleware(RequestIDMiddleware)

# Rate limiting (global)
app.add_middleware(RateLimitMiddleware, limit_per_minute=settings.rate_limit_per_minute)

# Routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(competition_router)
app.include_router(compat_router)
