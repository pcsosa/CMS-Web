#!/bin/bash
export DJANGO_SETTINGS_MODULE=cmsweb.settings.produccion
gunicorn --bind 127.0.0.1:8000 cmsweb.wsgi:application
