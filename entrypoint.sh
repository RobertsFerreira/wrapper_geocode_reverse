#!/bin/sh

poetry run alembic upgrade head

poetry run fastapi run wrapper_geocode_reverse/app.py --port=8080
