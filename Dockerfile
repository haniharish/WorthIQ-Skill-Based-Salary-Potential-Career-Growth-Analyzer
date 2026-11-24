# WorthIQ Production Backend Dockerfile
# Optimized for Render Web Service (Python 3.11 + Gunicorn + Scikit-Learn + SHAP + WhiteNoise)

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

# Install system dependencies needed for compiling C extensions, PostgreSQL, and OpenMP (XGBoost/LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy ML pipeline models, explainability artifacts, and code
COPY ml/ /app/ml/

# Copy Django backend application code
COPY backend/ /app/backend/

# Create media and static directories
RUN mkdir -p /app/backend/staticfiles /app/backend/media

# Create non-root application user for production security hardening
RUN useradd -m -u 1000 worthiq && \
    chown -R worthiq:worthiq /app

# Switch to backend directory for Django commands
WORKDIR /app/backend

# Make entrypoint executable
COPY docker-entrypoint.sh /app/backend/docker-entrypoint.sh
RUN chmod +x /app/backend/docker-entrypoint.sh && \
    chown worthiq:worthiq /app/backend/docker-entrypoint.sh

USER worthiq

# Expose port (Render dynamically sets $PORT environment variable)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health/ || exit 1

ENTRYPOINT ["/app/backend/docker-entrypoint.sh"]
