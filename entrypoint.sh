#!/usr/bin/env bash

export $(cat .env)
flask shell <<< "from autopsy_app.model import db; db.create_all();"
flask db stamp head && flask db migrate && flask db upgrade
uwsgi app.ini

