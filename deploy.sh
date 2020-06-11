#!/bin/sh

source env/bin/activate
cd Projet_08
git pull
python3.8 manage.py collectstatic --noinput --settings=Projet_08.settings.production
python3.8 manage.py migrate --settings=Projet_08.settings.production
/usr/bin/supervisorctl restart projet_08-gunicorn

