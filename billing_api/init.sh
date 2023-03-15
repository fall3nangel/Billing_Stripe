#!/bin/bash
set -exv

chmod +x *.sh
ls -l
wait_for.sh "${POSTGRES__HOST}:5432"
sed -i "s%sqlalchemy.url = postgresql://app:123qwe@127.0.0.1:5432/movies_database%sqlalchemy.url = postgresql://${POSTGRES__USER}:${POSTGRES__PASSWORD}@${POSTGRES__HOST}:5432/${POSTGRES__DB}%g" "alembic.ini"
alembic upgrade head
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8000