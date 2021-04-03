#!/bin/bash
docker build -t ep4sh/autopsy:$TRAVIS_TAG --build-arg FLASK_APP=$FLASK_APP --build-arg FLASK_ENV=$FLASK_ENV .
