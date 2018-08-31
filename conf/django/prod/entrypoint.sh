#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn knowledge.wsgi:application -w 2 -b :8000
