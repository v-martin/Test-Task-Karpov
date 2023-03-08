#!/bin/sh

until cd /api/TestTask
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


python manage.py collectstatic --noinput

gunicorn TestTask.wsgi --bind 0.0.0.0:8000