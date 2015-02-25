#!/usr/bin/env python3

import argparse, csv, sys, time, os, subprocess

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('size', type=str)
args = vars(parser.parse_args())

models = os.listdir('model')


workers = []
for model in models:
    prd_path = 'pool/{model}.r{size}.prd'.format(model=model, size=args['size'])
    if os.path.exists(prd_path):
        continue
    print('running {model}'.format(model=model))
    cmd = 'cd model/{model} && ./run.sh {size} && cp va.r{size}.prd ../../pool/{model}.r{size}.prd'.format(model=model, size=args['size'])
    worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    workers.append(worker)

for worker in workers:
    worker.communicate()
