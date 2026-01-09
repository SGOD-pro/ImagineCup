# ===============================
# Stage 1 — Build Frontend
# ===============================
FROM node:22-alpine AS frontend-builder

WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --force

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL


COPY frontend .
RUN npm run build


# ===============================
# Stage 2 — Backend + Nginx
# ===============================
FROM python:3.13.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install nginx
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx curl \
    && rm -rf /var/lib/apt/lists/*

# ---------------- Backend ----------------
WORKDIR /backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend .

# ---------------- Frontend (built assets only) ----------------
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html

# ---------------- Nginx config ----------------
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
