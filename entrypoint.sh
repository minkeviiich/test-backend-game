#!/bin/bash

python manage.py migrate
python create_superuser.py
python manage.py runserver 0.0.0.0:8000