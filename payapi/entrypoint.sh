#!/bin/bash
set -exv
gunicorn wsgi_app:app --workers 4 --worker-class gevent --bind 0.0.0.0:8000