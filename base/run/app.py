#!/usr/bin/env python3

import argparse, subprocess, sys, os, time, socket

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('size', type=str)
args = vars(parser.parse_args())

target = 'app'
size = args['size']

subprocess.call('./util/prepare.sh', stdout=subprocess.PIPE)

start = time.time()

cmd = 'util/parallelizer.py -s 24 converter/{target}.py tr.r{size}.app.csv va.r{size}.app.csv tr.r{size}.{target}.sp va.r{size}.{target}.sp'.format(size=size, target=target)
subprocess.call(cmd.split())

print('r{0} time used = {1:.0f}'.format(size, time.time()-start))

cmd = './mark1 -r 0.05 -s 24 -t 3 va.r{size}.{target}.sp tr.r{size}.{target}.sp'.format(size=size, target=target) 
subprocess.call(cmd.split())

cmd = './util/pickle_prediction.py va.r{size}.{target}.sp.prd va.r{size}.{target}.sp.prd.pickle'.format(size=size, target=target) 
subprocess.call(cmd.split())
