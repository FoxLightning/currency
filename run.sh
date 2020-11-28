#!/bin/bash

if [[ "$MODE" == "wsgi" ]]; then
  if [[ "$SERVER" == "dev" ]]; then
    python ./src/manage.py runserver 0:8000
  elif [[ "$SERVER" == "gunicorn" ]]; then
    gunicorn \
      -w $NUMBER_OF_WORKERS \
      -b $ADDRESS \
      --chdir /srv/project/src currency.wsgi \
      --timeout $TIMEOUT \
      --max-requests $MAX_REQUESTS
  else
    uwsgi --http $ADDRESS \
    --chdir /srv/project/src \
    --module currency.wsgi \
    --harakiri $TIMEOUT \
    --processes $NUMBER_OF_WORKERS \
    --max-requests $MAX_REQUESTS


  fi
elif [[ "$MODE" == "celery" ]]; then
  cd src && celery -A currency worker --autoscale=$MAX_N_WORKER,$MIN_N_WORKER -l INFO
elif [[ "$MODE" == "celerybeat" ]]; then
  cd src && celery -A currency beat -l INFO
else
  echo "NO SUCH MODE"
fi