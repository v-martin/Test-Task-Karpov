#!/bin/sh

until cd /api/TestTask
do
    echo "Waiting for server volume..."
done

celery -A TestTask worker --loglevel=info
