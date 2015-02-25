#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: run.sh <size>"
    exit 1
fi

util/run.template.py $1 A-site_category-f028772b 10
