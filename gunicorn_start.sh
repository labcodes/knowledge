#!/bin/bash

NAME="knowledge"
DJANGODIR=/home/labcodes/webapps/knowledge
SOCKFILE=/home/labcodes/webapps/knowledge/run/gunicorn.sock
USER=labcodes
GROUP=webapps
NUM_WORKERS=1
DJANGO_SETTINGS_MODULE=knowledge.settings
DJANGO_WSGI_MODULE=knowledge.wsgi
PORT=3333
TIMEOUT=120

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/labcodes/webapps/knowledge/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=unix:$SOCKFILE \
  --log-level=info \
  --log-file=- \
  --timeout $TIMEOUT \
  --bind=127.0.0.1:$PORT
