#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn dt.wsgi:application \
    --bind 0.0.0.0:8000 \
    --reload
    --workers 2