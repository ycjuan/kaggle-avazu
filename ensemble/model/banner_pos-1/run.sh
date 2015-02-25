#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: run.sh <size>"
    exit 1
fi

util/run.template.py $1 A-banner_pos-1 10
