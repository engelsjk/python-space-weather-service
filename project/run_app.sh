#!/bin/sh

export FLASK_APP=run.py
export FLASK_DEBUG=0
export FLASK_ENV=DEVELOPMENT

flask run -h 0.0.0.0