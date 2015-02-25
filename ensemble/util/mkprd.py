#!/usr/bin/env python3

import argparse, csv, sys

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('csv_path', type=str)
parser.add_argument('out_path', type=str)
parser.add_argument('prd_path', type=str)
args = vars(parser.parse_args())

with open(args['prd_path'], 'w') as f:
    f.write('id,click\n')

prd = {}
for csv_row, out_line in zip(csv.DictReader(open(args['csv_path'])), open(args['out_path'])):
    prd[csv_row['id']] = float(out_line.strip())

write_prd(prd, args['prd_path'])
