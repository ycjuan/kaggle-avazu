#!/usr/bin/env python3

import argparse, csv, sys, pickle, math

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('prd_path', type=str)
parser.add_argument('base_path', type=str)
parser.add_argument('ans_path', type=str)
args = vars(parser.parse_args())

prd = read_prd(args['prd_path'])
base_prd = read_prd(args['base_path'])
ans = {}
for row in csv.DictReader(open(args['ans_path'])):
    print(row['id'], row['click'])
    ans[row['id']] = float(row['click'])


loss, base_loss, total = 0.0, 0.0, 0
for key in set(prd.keys()).intersection(ans.keys()):
    if ans[key] == 1:
        loss += math.log(prd[key])
        base_loss += math.log(base_prd[key])
    else:
        loss += math.log(1-prd[key])
        base_loss += math.log(1-base_prd[key])
    total += 1

if total == 0:
    print('nan nan')
else:
    print('{0:.5f} {1:.5f}'.format(round(-loss/total, 5), round(-base_loss/total, 5)))
