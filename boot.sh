#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 -w 4 --access-logfile - --error-logfile - microblog:app
