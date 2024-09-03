web: gunicorn Soccer.wsgi --log-file -
worker: celery -A Soccer worker --loglevel=info
beat: celery -A Soccer beat --loglevel=info