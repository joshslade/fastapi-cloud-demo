# ---- 1. Build image -------------------------------------------------
FROM python:3.12-slim AS base

# (Optional) OS security patching
RUN apt-get update && apt-get -y upgrade && apt-get clean

WORKDIR /app

# Only copy requirements first for layer-cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- 2. Runtime image ----------------------------------------------
FROM base AS runtime

ENV PYTHONUNBUFFERED=1

# Copy the FastAPI source code
COPY . .

# Run with Gunicorn + Uvicorn workers (production best-practice)
CMD exec gunicorn -k uvicorn.workers.UvicornWorker \
      --bind :8080 --workers 2 app.main:app