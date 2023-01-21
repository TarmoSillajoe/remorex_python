#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

npm install
npm run build

python manage.py collectstatic --noinput
python manage.py compress --force
python manage.py collectstatic --noinput
python manage.py migrate