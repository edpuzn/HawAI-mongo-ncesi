# HawAI Monorepo

HawAI, SDG-3 (Sağlık ve Kaliteli Yaşam) odaklı bir yapay zekâ sağlık yardımcısıdır. Bu depo; FastAPI backend, Vue 3 + Vite frontend ve (opsiyonel) Dify entegrasyonunu içerir.

## Dizin Yapısı
- `HawAI-backend/` — FastAPI tabanlı API, model seed scriptleri ve Makefile hedefi
- `HawAI-frontend/` — Vue 3 + Vite + TypeScript arayüz
- `dify/` — Dify entegrasyonları ve örnekler (opsiyonel)

---

## Gereksinimler
- Python 3.11+
- Node.js 18+ (pnpm/yarn/npm)
- Docker (Ollama konteyneri için)
- curl, jq (kolay test için)

Ollama varsayılan erişim: `http://localhost:11434`

> Not: Ollama konteyner adı scriptte `hawai-ollama` olarak varsayılmıştır. Farklıysa `HawAI-backend/scripts/seed_ollama.sh` içindeki adı güncelleyin.

---

## Backend (FastAPI)

### 1) Kurulum
```bash
cd HawAI-backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` örneği:
```
OLLAMA_HOST=http://localhost:11434
MODEL_NAME=hawai-sdg3
ALLOWED_ORIGINS=http://localhost:5173
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_KEY_MODE=api_key_or_ip
LOG_LEVEL=INFO
WORKERS=1
```

### 2) Model Seed (Ollama)
```bash
# Tag’leri gör
curl -s http://localhost:11434/api/tags | jq .

# Modeli oluştur/seed et (8B, gerekirse 3B fallback)
bash scripts/seed_ollama.sh
# veya
make hawai-model
```
Beklenen model adı: `hawai-sdg3`.

Hızlı üretim testi:
```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "hawai-sdg3",
  "prompt": "Tip 2 diyabette beslenme için pratik öneriler verir misin?"
}' | jq -r '.response'
```

### 3) Çalıştırma
Geliştirme modu:
```bash
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Üretim benzeri (opsiyonel):
```bash
# WORKERS ve LOG_LEVEL .env’den okunur
gunicorn -k uvicorn.workers.UvicornWorker -w ${WORKERS:-2} -b 0.0.0.0:8000 app.main:app
```

### 4) Sağlık ve API Testleri
```bash
# Health
curl -s http://localhost:8000/healthz | jq .

# Basit chat testi
curl -s -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: demo-key' \
  -d '{"message":"Tip 2 diyabette beslenme için pratik öneriler?"}' | jq .
```

---

## Frontend (Vue 3 + Vite)
```bash
cd HawAI-frontend/frontend
# Paket yöneticinizi seçin (pnpm/yarn/npm)
pnpm i  # veya yarn / npm i

# .env
cat > .env <<EOT
VITE_API_URL=http://localhost:8000
VITE_API_KEY=demo-key
EOT

# Geliştirme sunucusu
pnpm run dev -- --host --port 5173  # veya eşdeğeri
```

Varsayılan adres: `http://localhost:5173`

---

## Makefile (Backend)
`HawAI-backend/Makefile` içinde model seed hedefi vardır:
```
.PHONY: hawai-model
hawai-model:
	@echo "[make] HawAI modeli Ollama’ya ekleniyor..."
	@bash scripts/seed_ollama.sh
	@echo "[make] Tamamlandı."
```

Kullanım:
```bash
cd HawAI-backend
make hawai-model
```

---

## Sorun Giderme
- Model bulunamadı: `MODEL_NAME=hawai-sdg3` ve `curl /api/tags` ile doğrulayın, `scripts/seed_ollama.sh` çalıştırın.
- OLLAMA_HOST ulaşılamıyor: Docker konteyner ve port mapping’i kontrol edin.
- CORS hatası: Backend `.env` içindeki `ALLOWED_ORIGINS`’i güncelleyin ve yeniden başlatın.
- 429 rate limit: `RATE_LIMIT_PER_MINUTE` değerini artırın veya bekleyip tekrar deneyin.
- API key: İstekte `X-API-Key` başlığını gönderin (örn. `demo-key`).

---

## Lisans
Bu depo içindeki her alt proje kendi lisans ve README’sine referans verebilir. Ayrıntılar için ilgili klasörleri inceleyin.
