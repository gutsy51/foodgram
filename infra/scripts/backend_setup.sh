#!/bin/bash
# Initialize Django backend: migrations and static files.
# WARNING: Run this script only from /infra/ directory.
# Usage: ./scripts/backend_setup.sh [--migrate] [--static]

set -e  # Exit immediately on error.

# Parse arguments.
DO_MIGRATE=true
DO_STATIC=true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-migrate) DO_MIGRATE=false ;;
        --no-static) DO_STATIC=false ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
    shift
done

# Validate Docker is running.
if ! docker compose ps --services | grep -q "backend"; then
    echo "Error: Backend container is not running. Run 'docker compose up -d' first." >&2
    exit 1
fi

# Apply migrations.
if $DO_MIGRATE; then
    echo "Applying migrations..."
    docker compose exec backend python foodgram/manage.py migrate --no-input
    echo "Migrated."
fi

# Collect static.
if $DO_STATIC; then
    echo "Collecting static files..."
    docker compose exec backend python foodgram/manage.py collectstatic --no-input --clear
    STATIC_SIZE=$(docker compose exec backend du -sh /app/foodgram/static | cut -f1)
    echo "Collected. Size: ${STATIC_SIZE}."
fi

echo -e "\n\033[32m✓ Backend ready\033[0m"