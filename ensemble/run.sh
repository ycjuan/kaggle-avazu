#!/bin/bash

mkdir -p data pool
make -C mark/mark1
ln -sf ../../base/base.r$1.prd pool/
ln -sf ../../bag/bag.r$1.prd pool/
ln -sf ../../tr.r$1.csv data/
ln -sf ../../va.r$1.csv data/

util/runall.py $1
util/ensemble.py $1
