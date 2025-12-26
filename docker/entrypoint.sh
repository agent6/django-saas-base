#!/usr/bin/env sh
set -e

python manage.py migrate
python manage.py ensure_initial_admin

exec "$@"
