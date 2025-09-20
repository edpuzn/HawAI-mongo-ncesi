FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn

COPY . .
EXPOSE 8000

CMD ["bash", "-lc", "gunicorn -k uvicorn.workers.UvicornWorker -w ${WORKERS:-1} -b 0.0.0.0:8000 app.main:app --access-logfile - --error-logfile - --log-level ${LOG_LEVEL,,} --forwarded-allow-ips='*' --proxy-allow-from='*'"]
