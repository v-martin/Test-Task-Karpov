#!/bin/sh

until cd /api/TestTask
do
    echo "Waiting for server volume..."
done

sleep 10

celery -A TestTask worker --loglevel=info
