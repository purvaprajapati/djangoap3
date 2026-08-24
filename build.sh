#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python clothing/manage.py collectstatic --no-input
python clothing/manage.py migrate
