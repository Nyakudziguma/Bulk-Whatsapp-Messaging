/usr/local/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8035 bulk_messaging.wsgi:application
