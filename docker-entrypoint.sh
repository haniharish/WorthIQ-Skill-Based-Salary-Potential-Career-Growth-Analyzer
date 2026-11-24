#!/bin/sh
set -e

echo "=== [WorthIQ Production Startup] ==="
echo "Port: ${PORT:-8000}"
echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files with WhiteNoise..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn WSGI production server..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile -
