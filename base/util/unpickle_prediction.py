#!/usr/bin/env python3

import argparse, sys, pickle

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser(description='process some integers')
parser.add_argument('src_path', type=str)
parser.add_argument('dst_path', type=str)
args = vars(parser.parse_args())

prd = pickle.load(open(args['src_path'], 'rb'))

with open(args['dst_path'], 'w') as f:
    f.write('id,click\n')
    for id, click in sorted(prd.items()):
        f.write('{0},{1}\n'.format(id,round(click, 5)))
