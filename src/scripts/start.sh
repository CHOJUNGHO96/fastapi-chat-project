#! /usr/bin/env sh
set -e

if [ -f /fastapi-chat-project/src/main.py ]; then
    DEFAULT_MODULE_NAME=src.main
elif [ -f /fastapi-chat-project/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

if [ -f /fastapi-chat-project/src/gunicorn/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/fastapi-chat-project/src/gunicorn/gunicorn_conf.py
elif [ -f /fastapi-chat-project/gunicorn/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/fastapi-chat-project/gunicorn/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi

export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Start Gunicorn
exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE"