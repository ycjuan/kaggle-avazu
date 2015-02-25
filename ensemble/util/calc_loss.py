#!/usr/bin/env python3

import argparse, csv, sys, pickle, math

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('prd_path', type=str)
parser.add_argument('ans_path', type=str)
args = vars(parser.parse_args())

prd = read_prd(args['prd_path'])
ans = {}
for row in csv.DictReader(open(args['ans_path'])):
    ans[row['id']] = float(row['click'])

if len(prd) < len(ans):
    print('Warning: it is not a full prediction')

loss, total = 0.0, 0
for key in set(prd.keys()).intersection(ans.keys()):
    if ans[key] == 1:
        loss += math.log(prd[key])
    else:
        loss += math.log(1-prd[key])
    total += 1

if total == 0:
    print('nan')
else:
    print(round(-loss/total, 5))
