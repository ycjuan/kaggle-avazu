#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: run.sh <size>"
    exit 1
fi

util/run.template.py $1 A-site_domain-7e091613 3
