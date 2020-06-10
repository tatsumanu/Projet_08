#!/bin/sh

source env/bin/activate
cd Projet_08
git pull
python3.8 manage.py collectstatic --settings=Projet_08.settings.production
python3.8 manage.py migrate
/usr/bin/supervisorctl restart projet_08-gunicorn

