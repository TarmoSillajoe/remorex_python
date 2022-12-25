#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

npm install
npm run watch

python manage.py collectstatic --no-input
python manage.py migrate
