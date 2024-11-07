#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status.

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Navigate to the correct directory for alembic.ini
cd /home/app/web

# Run migrations
alembic upgrade head

exec "$@"
