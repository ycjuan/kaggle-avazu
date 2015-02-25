#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: run.sh <size>"
    exit 1
fi

util/run.template.py --reg 0.0005 --eta 0.02 $1 A-site_id-e151e245 14
