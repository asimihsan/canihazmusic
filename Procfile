web: gunicorn canihazmusic.wsgi -b 0.0.0.0:$PORT
celeryd: python -u manage.py celeryd --concurrency 1 --purge --beat --events --maxtasksperchild=4 --soft-time-limit=30 --time-limit=60 --loglevel=INFO --no-execv

