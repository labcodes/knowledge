#!/usr/bin/env bash

python manage.py migrate --settings=knowledge.settings

python manage.py runserver 0.0.0.0:8000 --settings=knowledge.settings
