# syntax=docker/dockerfile:1

############################################
# Base stage
############################################
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && rm -rf /var/lib/apt/lists/*

# Copy requirements & install
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy backend source
COPY main.py database.py ai_processor.py ./
COPY frontend ./frontend
COPY sample_data ./sample_data
COPY README.md .

# Build frontend (production) if package.json exists
FROM node:20-alpine AS frontendbuild
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install || true
COPY frontend ./
RUN npm run build || echo "Frontend build skipped"

# Final image
FROM base AS final
ENV PORT=8000 \
    HOST=0.0.0.0

# Copy built frontend if available
COPY --from=frontendbuild /frontend/dist ./frontend/dist

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
