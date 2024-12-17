#!/usr/bin/env bash

docker run -it -v $(pwd):/srv $(docker build -q .) python /srv/parse_postal_address.py
