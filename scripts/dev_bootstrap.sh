#!/usr/bin/env bash
set -e

python -m venv .venv
. .venv/bin/activate
pip install -U pip
