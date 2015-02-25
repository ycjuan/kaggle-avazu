#!/usr/bin/env python3

import argparse, csv, sys, pickle, collections, math

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser(description='process some integers')
parser.add_argument('prd_paths', nargs='+', type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

def logistic_func(x):
    return 1/(1+math.exp(-x))

def inv_logistic_func(x):
    return math.log(x/(1-x))

mprd = collections.defaultdict(list)
for path in args['prd_paths']:
    prd = pickle.load(open(path, 'rb'))
    for key, value in prd.items():
        mprd[key].append(value)

for key in mprd:
    mprd[key] = logistic_func(sum(map(inv_logistic_func, mprd[key]))/len(mprd[key]))

pickle.dump(mprd, open(args['out_path'], 'wb'))
