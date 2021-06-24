#!/bin/bash
docker-compose down
cd printerbox_cupsd/ && ./docker_build.sh && cd - && docker-compose build
docker-compose up -d cupsd

