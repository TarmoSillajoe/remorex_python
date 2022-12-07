#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
npm install
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css

python manage.py collectstatic --no-input
python manage.py migrate
