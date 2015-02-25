#!/usr/bin/env python3
import argparse

def parse_args():
	parser = argparse.ArgumentParser('concatenate two disjoint submissions')
	parser.add_argument('sub0', type=str, help='one submission file')
	parser.add_argument('sub1', type=str, help='the other submission file')
	parser.add_argument('concated', type=str, help='path to the concantenated submission') 
	return vars(parser.parse_args())

if __name__ == '__main__':
	args = parse_args()
	with open(args['sub0'], 'rt') as fh0, open(args['sub1'], 'rt') as fh1, open(args['concated'], 'wt') as fout:
		for line in fh0:
			fout.write(line)
		fh1.readline() # drop the header of the second file
		for line in fh1:
			fout.write(line)
