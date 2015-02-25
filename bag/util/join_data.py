#!/usr/bin/env python3
import argparse
import pandas as pd

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('raw')
	parser.add_argument('join')
	return vars(parser.parse_args())

if __name__ == '__main__':
	args = parse_args()
	to_join = dict()
	with open(args['join'], 'rt') as fh:
		for line in fh:
			x = line.rstrip().split(' ', 1)
			to_join[x[0]] = x[1] if len(x) == 2 else ''
	with open(args['raw'], 'rt') as fi, open(args['raw']+'.join', 'wt') as fo:
		for line in fi:
			i, ins = line.rstrip().split(' ', 1)
			fo.write(ins + ' ' + to_join[i] + '\n')
