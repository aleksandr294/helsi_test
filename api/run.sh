#!/bin/bash

python manage.py migrate
python manage.py test_user
python manage.py runserver 0.0.0.0:8000