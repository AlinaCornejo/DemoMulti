#!/bin/bash

# 1. Aplicar migraciones compartidas
echo "=== Aplicando migraciones compartidas ==="
python manage.py makemigrations --noinput  # Solo si necesitas crear migraciones
python manage.py migrate_schemas --shared

# 2. Verificar/Crear tenant público
echo "=== Verificando tenant público ==="
if ! python manage.py tenant_exists public; then
  echo "--- Creando tenant público ---"
  python manage.py create_tenant \
    --schema_name=public \
    --name="Public" \
    --domain=${RAILWAY_STATIC_URL} \
    --client_domain=${RAILWAY_STATIC_URL}
else
  echo "El tenant público ya existe"
fi

# 3. Aplicar migraciones para todos los tenants
echo "=== Aplicando migraciones para todos los tenants ==="
python manage.py migrate_schemas

# 4. Iniciar servidor
echo "=== Iniciando Gunicorn ==="
exec gunicorn DemoMultitenant.wsgi \
  --workers ${GUNICORN_WORKERS:-2} \
  --timeout 120 \
  --bind 0.0.0.0:${PORT:-8000} \
  --access-logfile - \
  --error-logfile -