#!/bin/sh
# Configuración robusta de PATH
export PATH="/opt/venv/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# Verificación explícita de Python
PYTHON_CMD=$(command -v python3 || command -v python)
if [ -z "$PYTHON_CMD" ]; then
  echo "ERROR: Python no está instalado o no está en el PATH"
  exit 1
fi

# 1. Migraciones compartidas
$PYTHON_CMD manage.py migrate_schemas --shared

# 2. Crear tenant público
$PYTHON_CMD manage.py create_tenant \
  --schema_name=public \
  --name="Public" \
  --domain=${RAILWAY_STATIC_URL:-localhost}

# 3. Migraciones para tenants
$PYTHON_CMD manage.py migrate_schemas

# 4. Iniciar servidor
exec gunicorn DemoMultitenant.wsgi \
  --workers ${GUNICORN_WORKERS:-2} \
  --timeout 120 \
  --bind 0.0.0.0:${PORT:-8000}
