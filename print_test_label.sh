#!/bin/bash
docker-compose run --rm  --volume /home/pi/printerbox_sortkaffe/test_labels:/test_labels --entrypoint python sortkaffe /src/print_label.py $1 $2
