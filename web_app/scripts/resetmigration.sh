#!/bin/sh
alembic downgrade base
rm migrations/versions/*
alembic revision --autogenerate -m"Initial DB"
alembic upgrade head
python ./web_app/scripts/initializedb.py