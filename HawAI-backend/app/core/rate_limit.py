import time
import inspect
from functools import wraps
from typing import Callable, Optional, Tuple
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from app.core.config import settings


RATE_LIMIT_MESSAGE = {"detail": "rate limit exceeded"}


def _get_client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def select_rate_limit_key(request: Request) -> str:
    mode = (settings.rate_limit_key_mode or "api_key_or_ip").lower()
    api_key = request.headers.get("x-api-key")
    if mode == "api_key":
        return api_key or "anonymous"
    if mode == "ip":
        return _get_client_ip(request)
    # default: api_key_or_ip
    return api_key or _get_client_ip(request)


def parse_rate(rate: str) -> Tuple[int, int]:
    # Only supports like "60/minute" for now
    parts = rate.split("/")
    count = int(parts[0])
    window = 60
    return count, window


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self.buckets: dict[str, list[float]] = {}

    def check_and_increment(self, key: str, limit: int, window: int) -> bool:
        now = time.time()
        bucket = self.buckets.setdefault(key, [])
        cutoff = now - window
        # prune old
        i = 0
        for ts in bucket:
            if ts >= cutoff:
                break
            i += 1
        if i:
            del bucket[:i]
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True


_shared_limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_minute: int = 60):
        super().__init__(app)
        self.limit = max(1, int(limit_per_minute))
        self.window = 60
        self.limiter = _shared_limiter

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        key = select_rate_limit_key(request)
        allowed = self.limiter.check_and_increment(key, self.limit, self.window)
        if not allowed:
            return JSONResponse(RATE_LIMIT_MESSAGE, status_code=429)
        return await call_next(request)


class Limiter:
    def __init__(self, limiter: Optional[InMemoryRateLimiter] = None) -> None:
        self._limiter = limiter or _shared_limiter

    def limit(self, rate: str) -> Callable:
        limit_count, window = parse_rate(rate)

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):  # type: ignore[no-untyped-def]
                # Expect FastAPI to pass Request via kwargs or find in args
                request: Optional[Request] = kwargs.get("request") if isinstance(kwargs.get("request"), Request) else None
                if request is None:
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break
                if request is None:
                    return await func(*args, **kwargs)
                key = select_rate_limit_key(request)
                allowed = self._limiter.check_and_increment(key, limit_count, window)
                if not allowed:
                    return JSONResponse(RATE_LIMIT_MESSAGE, status_code=429)
                return await func(*args, **kwargs)

            # Preserve original signature for FastAPI
            try:
                wrapper.__signature__ = inspect.signature(func)  # type: ignore[attr-defined]
            except Exception:
                pass
            return wrapper

        return decorator


limiter = Limiter(_shared_limiter)
