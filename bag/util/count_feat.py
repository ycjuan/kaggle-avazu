#!/usr/bin/env python3
import argparse
import pandas as pd
import pickle

def parse_args():
	parser = argparse.ArgumentParser('count the occurences of all features')
	parser.add_argument('tr_path', type=str, help='path to training set in CSV format')
	parser.add_argument('va_path', type=str, help='path to test set in CSV format')
	parser.add_argument('min_occur', type=int, help='set the minimum occurence of the considered features')
	parser.add_argument('cnt_path', type=str, help='path to the counting result') 
	return vars(parser.parse_args())

if __name__ == '__main__':
	args = parse_args()
	tr = pd.read_csv(args['tr_path'], dtype=str)
	va = pd.read_csv(args['va_path'], dtype=str)

	trva = pd.concat([tr, va])

	group_counts = dict()

	min_occur = args['min_occur']

	nr_feats = 0
	for field in trva.columns:
		cnts = trva[field].value_counts()
		group_counts[field] = cnts[cnts >= min_occur].to_dict()
		nr_feats += len(group_counts[field])

	with open(args['cnt_path'], 'wb') as fh:
		pickle.dump(group_counts, fh) 
