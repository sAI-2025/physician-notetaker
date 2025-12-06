
#!/usr/bin/env bash
set -e

echo "===== Starting Jupiter FAQ Bot Application ====="
echo "Current time: $(date)"
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"

# Navigate to the Django project directory
cd /app/physician-notetaker

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn server on port 7860..."
exec gunicorn chatbot_project.wsgi:application \
  --bind 0.0.0.0:7860 \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  --worker-class gthread \
  --worker-tmp-dir /dev/shm \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  --capture-output \
  --enable-stdio-inheritance
