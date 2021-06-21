#!/bin/bash
docker-compose run --entrypoint python sortkaffe /src/print_label.py $1
