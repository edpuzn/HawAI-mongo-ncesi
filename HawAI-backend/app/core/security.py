from typing import Dict, List
from app.core.config import Settings


def get_cors_config(settings: Settings) -> Dict[str, object]:
    allow_origins: List[str] = settings.allowed_origins
    wildcard = "*" in allow_origins
    allow_credentials: bool = False if wildcard else True
    return {
        "allow_origins": allow_origins,
        "allow_credentials": allow_credentials,
    }
