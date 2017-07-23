#!/bin/bash
# Prepare log files and start outputting logs to stdout
# mkdir -p /usr/local/var/log/uwsgi

touch whatsinmyfridge.log
chmod 644 whatsinmyfridge.log

# Webapp commands
python3 manage.py makemigrations
./wait-for-it.sh postgres:5432 -- echo "Postgres is up for uwsgi and nginx"
python3 manage.py migrate                  # Apply database migrations
# python3 manage.py loaddata fixtures/latest.json
python3 manage.py collectstatic --noinput  # Collect static files
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
