#!/bin/bash
envsubst '\$NGINX_PORT' < default.conf > /etc/nginx/sites-enabled/default
sed -i "s/^worker_processes.*/worker_processes $NGINX_PROCESSES;/" /etc/nginx/nginx.conf

python3 manage.py migrate
python3 manage.py collectstatic --noinput

exec "$@"
