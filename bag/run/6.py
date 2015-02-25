#!/usr/bin/env python3

import argparse, subprocess, sys, os, time, socket

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('category', type=str)
parser.add_argument('size', type=str)
args = vars(parser.parse_args())

CATEGORY = args['category']
SIZE = args['size']

start = time.time()

cmd = 'util/parallelizer.py -s 24 converter/6.py tr.r{size}.{category}.new.csv va.r{size}.{category}.new.csv tr.r{size}.{category}.sp va.r{size}.{category}.sp'.format(size=SIZE, category=CATEGORY)
subprocess.call(cmd.split())

cmd = 'converter/group6.py tr.r{size}.{category}.new.csv va.r{size}.{category}.new.csv {category} device_id pub_id,pub_domain '.format(size=SIZE, category=CATEGORY)
subprocess.call(cmd.split())

cmd = 'util/join_data.py tr.r{size}.{category}.sp tr.r{size}.{category}.new.csv.group'.format(size=SIZE, category=CATEGORY)
subprocess.call(cmd.split())

cmd = 'util/join_data.py va.r{size}.{category}.sp va.r{size}.{category}.new.csv.group'.format(size=SIZE, category=CATEGORY)
subprocess.call(cmd.split())

print('time used = {0:.0f}'.format(time.time()-start))

cmd = './mark18 -r 0.05 -s 1 -t 6 va.r{size}.{category}.sp.join tr.r{size}.{category}.sp.join'.format(size=SIZE, category=CATEGORY) 
subprocess.call(cmd.split())

cmd = './util/cat_id_click.py va.r{size}.{category}.sp va.r{size}.{category}.sp.join.out va.r{size}.{category}.submit'.format(size=SIZE, category=CATEGORY) 
subprocess.call(cmd.split())
