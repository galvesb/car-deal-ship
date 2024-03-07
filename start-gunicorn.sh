#!/usr/bin/env bash
set -e

[[ $DEBUG ]] && set -x

export GUNICORN_CONFIG=${GUNICORN_CONFIG:-devtools/gunicorn_config.py}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}
export APP_MODULE=${1:-api_main:create_app()}
export GUNICORN_EXTRAS=${GUNICORN_EXTRAS:-""}

exec $APM_RUN gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONFIG" "$APP_MODULE" $GUNICORN_EXTRAS
