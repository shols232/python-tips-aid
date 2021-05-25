web: gunicorn twitter_help.wsgi --log-file -
worker: celery -A twitter_help worker --beat -S django --loglevel info