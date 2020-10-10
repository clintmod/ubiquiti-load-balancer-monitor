#!/usr/bin/env bash


set -e 

python -V | grep `cat .python-version`
.venv/bin/deactivate || true
if ! which poetry; then
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
fi
pip install --upgrade pip
poetry install
