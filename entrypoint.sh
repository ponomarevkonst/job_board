#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc - db 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
python manage.py makemigrations 
python manage.py migrate
python manage.py populate_db
exec "$@"
