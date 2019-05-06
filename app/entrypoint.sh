#!/usr/bin/env bash
python /opt/semantive/manage.py migrate --noinput && python /opt/semantive/manage.py runserver 0.0.0.0:8000