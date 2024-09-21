#!/bin/sh

poetry run alembic upgrade --head

oetry run fastapi run wrapper_geocode_reverse/app.py