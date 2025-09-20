# HawAI-backend

HawAI (SDG-3 Health Guide) icin production-grade FastAPI backend.

## Quickstart

Gereksinimler: Python 3.11+

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Testler:
```bash
pytest -q
```

## Ortam Degiskenleri
- `OLLAMA_HOST`: or. `http://localhost:11434`
- `MODEL_NAME`: or. `llama3.1:8b`
- `ALLOWED_ORIGINS`: CSV, or. `http://localhost:3000,https://example.com`
- `RATE_LIMIT_PER_MINUTE`: tamsayi, or. `60`
- `RATE_LIMIT_KEY_MODE`: `ip` | `api_key` | `api_key_or_ip`
- `LOG_LEVEL`: `INFO` (varsayilan)
- `WORKERS`: `1` (varsayilan)

### Rate Limiting Notlari
- Varsayilan anahtar modu: `api_key_or_ip`.
- API anahtari gondermek icin header kullanin: `X-API-Key: <your-key>`.
- Uretimde API Gateway ile anahtar uretimi/dagitimi onerilir.

## Docker
```bash
# Build
docker build -t hawai-backend:latest .
# Run (Gunicorn + UvicornWorker, log seviyesi ve worker sayisi ENV'den)
docker run --rm -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  -e MODEL_NAME=llama3.1:8b \
  -e LOG_LEVEL=INFO \
  -e WORKERS=2 \
  hawai-backend:latest
```

## Endpointler
- GET `/healthz`
- POST `/chat`

Ozellikler: async mimari, JSON loglama + X-Request-ID, in-memory rate limiting, basit SDG siniflandirma, statik kaynaklar.
