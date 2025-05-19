#!/bin/bash

# 1. Configurar entorno
export PATH="/opt/venv/bin:$PATH"

# 2. Verificar dependencias
if ! command -v python &> /dev/null; then
  echo "Python no encontrado, buscando alternativas..."
  if command -v python3 &> /dev/null; then
    alias python=python3
  else
    echo "ERROR: Python no está instalado"
    exit 1
  fi
fi

# 3. Migraciones
python manage.py migrate_schemas --shared

# 4. Crear tenant
python manage.py create_tenant \
  --schema_name=public \
  --name="Public" \
  --domain=${RAILWAY_STATIC_URL:-localhost} \
  --client_domain=${RAILWAY_STATIC_URL:-localhost}

# 5. Migraciones para tenants
python manage.py migrate_schemas

# 6. Iniciar servidor
exec gunicorn DemoMultitenant.wsgi \
  --workers ${GUNICORN_WORKERS:-2} \
  --timeout 120 \
  --bind 0.0.0.0:${PORT:-8000}