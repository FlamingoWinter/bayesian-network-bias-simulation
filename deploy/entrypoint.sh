#!/bin/bash
set -eu

cd /app/backend/api
python manage.py migrate --noinput

daphne -b 127.0.0.1 -p 8000 server.routing:application &
nginx -g 'daemon off;' &

# Exit if either process dies (e.g. daphne OOM-killed) so Docker restarts the container.
trap 'kill $(jobs -p) 2>/dev/null || true' TERM INT
status=0
wait -n || status=$?
kill $(jobs -p) 2>/dev/null || true
exit "${status:-1}"
