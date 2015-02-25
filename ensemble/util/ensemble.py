#!/usr/bin/env python3

import argparse, csv, sys, time, os, subprocess

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('size', type=str)
args = vars(parser.parse_args())

prd_paths, workers = [], {}

for prd_path in os.listdir('pool'):
    if '.r{0}.'.format(args['size']) not in prd_path:
        continue
    prd_path = 'pool/'+prd_path
    prd_paths.append(prd_path)
    #if args['size'] != '0':
    #    cmd = 'util/calc_loss2.py {prd_path} pool/base.r{size}.prd data/va.r{size}.csv'.format(prd_path=prd_path, size=args['size'])
    #    worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #    workers[prd_path] = worker

runcmd('util/merge_prd.py {prds} r{size}.prd'.format(prds=' '.join(prd_paths), size=args['size']))

if args['size'] != '0':
    cmd = 'util/calc_loss.py r{size}.prd data/va.r{size}.csv'.format(size=args['size'])
    worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    loss = worker.communicate()[0].decode('utf-8').strip()
    print('loss = {0}'.format(loss))

    #for prd_path in workers:
    #    worker = workers[prd_path]
    #    loss, base_loss = worker.communicate()[0].decode('utf-8').split()
    #    print('{model:30} {loss:>10} {base_loss:>10}'.format(model=os.path.basename(prd_path), loss=loss, base_loss=base_loss))
