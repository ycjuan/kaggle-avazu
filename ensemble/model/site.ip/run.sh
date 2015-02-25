#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: run.sh <size>"
    exit 1
fi

util/run.template.py $1 B-site_id-85f751fd,A-device_id-a99f214a 8
