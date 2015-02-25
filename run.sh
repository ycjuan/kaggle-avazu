#!/bin/bash

cd base
./run.py $1
cd ..

cp base/base.r$1.prd .
