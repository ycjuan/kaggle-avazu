#!/usr/bin/env python3

import argparse, csv, sys, pickle

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser(description='process some integers')
parser.add_argument('prd_path', type=str)
parser.add_argument('out_path', type=str)
args = vars(parser.parse_args())

prd = {}
for row in csv.DictReader(open(args['prd_path']), delimiter=','):
    prd[row['id']] = float(row['click'])

pickle.dump(prd, open(args['out_path'], 'wb'))
