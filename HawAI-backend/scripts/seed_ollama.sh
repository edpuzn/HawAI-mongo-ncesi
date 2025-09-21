#!/usr/bin/env bash
set -euo pipefail

TAGS_JSON="$(curl -s http://localhost:11434/api/tags || true)"
if echo "$TAGS_JSON" | grep -q '"name":"hawai-sdg3"'; then
  echo "[seed] hawai-sdg3 zaten mevcut."
  exit 0
fi

echo "[seed] hawai-sdg3 (8B) modeli build ediliyor..."
docker cp models/hawai/Modelfile hawai-ollama:/tmp/Modelfile || true
if ! docker exec -it hawai-ollama ollama create hawai-sdg3 -f /tmp/Modelfile; then
  echo "[seed] 8B build başarısız, 3B fallback deneniyor..."
  docker cp models/hawai/Modelfile.3b hawai-ollama:/tmp/Modelfile.3b || true
  docker exec -it hawai-ollama ollama create hawai-sdg3 -f /tmp/Modelfile.3b
fi

echo "[seed] doğrulama..."
curl -s http://localhost:11434/api/tags | jq .
