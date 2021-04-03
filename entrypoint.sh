#!/usr/bin/env bash

export $(cat .env)
flask db migrate && flask db upgrade
uwsgi app.ini

