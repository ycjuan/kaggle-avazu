#!/usr/bin/env python3
import argparse
import sys

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('ins_feat', type=str)
	parser.add_argument('pred', type=str)
	parser.add_argument('submit', type=str)
	return vars(parser.parse_args())

if __name__ == '__main__':
	args = parse_args()
	with open(args['ins_feat'], 'rt') as fi, open(args['pred'], 'rt') as fp, open(args['submit'], 'wt') as fs:
		fs.write('id,click\n')
		for li, lp in zip(fi, fp):
			i, feat = li.rstrip().split(' ', 1)
			clk = lp.rstrip()
			fs.write('{i},{click}\n'.format(i=i, click=clk))
