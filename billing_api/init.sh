#!/bin/bash
set -exv

chmod +x *.sh
ls -l
wait_for.sh "${POSTGRES__HOST}:5432"
alembic upgrade head
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8000