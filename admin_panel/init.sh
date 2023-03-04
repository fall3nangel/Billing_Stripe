#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

python3 manage.py migrate
python3 manage.py createsuperuser --noinput || true
python3 manage.py compilemessages -l en -l ru


uwsgi --strict --ini uwsgi/uwsgi.ini
