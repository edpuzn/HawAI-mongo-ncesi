# Competition Analysis (HawAI)

Bu dosya proje içinde `GET /competition/` endpoint'inden alınan statik verinin açıklamasını içerir.

## Nasıl çalışır
- `data/competition.json` dosyası statik rekabet verisini tutar.
- Backend `services/competition.py` router'ı bu JSON'u `GET /competition/` ile döner.
- Frontend `CompetitionTable.vue` bileşeni bu endpoint'i çağırır ve Bootstrap tablosunda gösterir.

## Geliştirme notları
- Yeni rakip eklemek için `data/competition.json` dosyasını güncelleyin.
- Daha zengin karşılaştırma (puanlama, feature flags) gerekiyorsa backend içinde küçük bir skorlayıcı ekleyin.
