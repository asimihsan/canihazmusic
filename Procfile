web: gunicorn canihazmusic.wsgi -b 0.0.0.0:$PORT
celeryd: python -u manage.py celeryd --autoscale=1,0 --purge --beat --events --soft-time-limit=30 --time-limit=60 --loglevel=INFO

