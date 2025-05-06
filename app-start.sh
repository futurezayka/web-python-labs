#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace
python manage.py migrate
#python manage.py collectstatic --noinput

#uvicorn core.asgi:application --host 0.0.0.0 --port 8000
python manage.py runserver 0.0.0.0:8000
