#!/usr/bin/env python3

import argparse, subprocess, sys, os, time, socket

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('--reg', dest='reg', type=float, default=0.00002)
parser.add_argument('--eta', dest='eta', type=float, default=0.05)
parser.add_argument('--mark', dest='mark', type=str, default='mark1')
parser.add_argument('size', type=str)
parser.add_argument('filter_string', type=str)
parser.add_argument('iter', type=str)
args = vars(parser.parse_args())

##################################################

start = time.time()

runcmd('util/subset.py {filter_string} data/tr.r{size}.csv data/va.r{size}.csv tr.r{size}.sub.csv va.r{size}.sub.csv'.format(filter_string=args['filter_string'], size=args['size']))

runcmd('util/gendata.py tr.r{size}.sub.csv va.r{size}.sub.csv tr.r{size}.new.csv va.r{size}.new.csv'.format(size=args['size']))

for dataset in ['tr', 'va']:
    runcmd('./cvt.py {dataset}.r{size}.new.csv {dataset}.r{size}.sp'.format(dataset=dataset, size=args['size']))

runcmd('mark/{mark}/{mark} -t {iter} -l {reg} -r {eta} va.r{size}.sp tr.r{size}.sp va.r{size}.out'.format(iter=args['iter'], size=args['size'], reg=args['reg'], eta=args['eta'], mark=args['mark']))

runcmd('util/mkprd.py va.r{size}.sub.csv va.r{size}.out va.r{size}.prd'.format(size=args['size']))
runcmd('util/calc_loss.py va.r{size}.prd va.r{size}.sub.csv'.format(size=args['size']))
