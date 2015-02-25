#!/bin/bash

cd base
./run.py $1
cd ..

cd bag
./run.sh $1
cd ..

cd ensemble
./run.sh $1
cd ..

cp ensemble/r$1.prd .
