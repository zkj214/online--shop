#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate



if [[ $CREATE_SUPERUSER ]];
then
  python world_champ_2022/manage.py createsuperuser --no-input
fi
