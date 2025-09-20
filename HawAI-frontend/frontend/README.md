# HawAI-frontend

Production-grade Vue 3 + Vite + TypeScript frontend for HawAI.

## Kurulum
```bash
npm i
cp .env.example .env
```

## .env
```
VITE_API_URL=http://localhost:8000
VITE_API_KEY=demo-key
```

## Komutlar
```bash
npm run dev      # geliştirici sunucu
npm run build    # prod build (dist/)
npm run preview  # dist önizleme
npm run lint     # ESLint
```

## Docker
```bash
# Build
docker build -t hawai-frontend:latest .
# Run
docker run --rm -p 8080:80 --env-file .env hawai-frontend:latest
```

## Deploy Notları
- Nginx ile SPA yönlendirmesi `try_files $uri /index.html` yapılandırıldı.
- API URL ve anahtar `.env` ile gelir; reverse proxy üzerinden CORS ve güvenlik ayarları uygulanmalıdır.
- 429 oran sınırlama durumlarında toast uyarısı gösterilir.
```
