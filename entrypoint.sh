#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc - db 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py makemigrations jobs
python manage.py makemigrations account
python manage.py migrate jobs
python manage.py migrate account
python manage.py init_data
exec "$@"
