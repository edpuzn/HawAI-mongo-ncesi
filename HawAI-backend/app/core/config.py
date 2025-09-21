import os
from dataclasses import dataclass
from typing import List


def _parse_origins(value: str | None) -> List[str]:
    if not value:
        return ["*"]
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return parts or ["*"]


@dataclass
class Settings:
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name: str = os.getenv("MODEL_NAME", "hawai-sdg3")
    system_prompt: str | None = os.getenv("SYSTEM_PROMPT")
    compat_api_key: str | None = os.getenv("COMPAT_API_KEY", "demo-key")
    allowed_origins: List[str] = None  # type: ignore[assignment]
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    # New
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    workers: int = int(os.getenv("WORKERS", "1"))
    rate_limit_key_mode: str = os.getenv("RATE_LIMIT_KEY_MODE", "api_key_or_ip")

    def __post_init__(self) -> None:
        self.allowed_origins = _parse_origins(os.getenv("ALLOWED_ORIGINS"))


settings = Settings()
