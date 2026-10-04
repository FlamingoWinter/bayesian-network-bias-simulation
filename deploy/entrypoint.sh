#!/bin/sh
set -eu

cd /app/backend/api
python manage.py migrate --noinput

daphne -b 127.0.0.1 -p 8000 server.routing:application &
exec nginx -g 'daemon off;'
