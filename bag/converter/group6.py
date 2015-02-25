#!/usr/bin/env python3
import argparse
import copy
import hashlib
import itertools
import math
import multiprocessing
import numpy as np
import os
import pandas as pd
import pickle
import random
import time
from multiprocessing import Pool 
import subprocess
from collections import defaultdict
from collections import Counter

f_fields = ['hour', 'banner_pos', 'device_id', 'device_ip', 'device_model', 'device_conn_type', 'C14', 'C17', 'C20', 'C21', 'pub_id', 'pub_domain', 'pub_category', 'device_id_count', 'device_ip_count', 'user_count', 'smooth_user_hour_count', 'user_click_histroy']

def parse_args():
	parser = argparse.ArgumentParser('Calculate group features and dump them to a specified file')
	parser.add_argument('train', type=str, help='csv file')
	parser.add_argument('valid', type=str, help='csv file')
	parser.add_argument('partition', type=str, help='site/app')
	parser.add_argument('g_field', type=str, help='specified the fields used to group instances')
	parser.add_argument('a_field', type=str, help='specified the fields considered in each group')
	parser.add_argument('--gc_begin', type=int, default=16, help='the index of the first column in group features')
	parser.add_argument('--max_occur', type=int, default=100, help='specified the maximum number of count features. Any feature with counts less than the value would be replaced with its count.')
	parser.add_argument('--max_sz_group', type=int, default=100, help='the upper limit of the size of each group')
	parser.add_argument('--max_nr_group_feats', type=int, default=2500, help='the maximum number of features among a group')
	return vars(parser.parse_args())

def hashstr(str, nr_bins=1e6):
    return int(hashlib.md5(str.encode('utf8')).hexdigest(), 16)%(nr_bins-1)+1

def vtform(v, partition, c, cnts, max_occur):
	pub_in_raw = {'pub_id': {'app': 'app_id', 'site': 'site_id'}, 'pub_domain': {'app': 'app_domain', 'site': 'site_domain'}, 'pub_category': {'app': 'app_category', 'site': 'site_category'}}
	if c in pub_in_raw:
		c = pub_in_raw[c][partition]
	if c != 'hour':
		if v in cnts[c]:
			if cnts[c][v] >= max_occur:
				return c+'-'+v
			else:
				return c+'-less-'+str(cnts[c][v])
		else:
			return c+'-less'
	else:
		return c+'-'+v[-2:]

def generate_feats(df, partition, a_field, gc_begin, max_occur, max_sz_group, max_nr_group_feats, tr_path, va_path):
	g_added = set(a_field.split(',')) & set(f_fields)
	col_fm_indices = {c:i+gc_begin for i, c in enumerate(g_added)}
	with open('fc.trva.r0.t2.pkl', 'rb') as fh:
		cnts = pickle.load(fh)
	with open(tr_path, 'wt') as f_tr, open(va_path, 'wt') as f_va:
		for gid, group in df.groupby('__kid__'):
			group_feats = dict()
			if len(group) < max_sz_group:
				for c in g_added:
					group_feats[c] = Counter(group[c].apply(lambda x: vtform(x, partition, c, cnts, max_occur)))
					c_norm = 1/math.sqrt(sum([w**2 for w in group_feats[c].values()]))/len(g_added)
					for v, w in group_feats[c].items():
						group_feats[c][v] = w*c_norm
			
			gf_str = ''
			for c, vws in group_feats.items():
				for v, w in vws.items():
					gf_str += ' {0}:{1}:{2:.5f}'.format(col_fm_indices[c], int(hashstr('group-'+v)), w)

			for rid, row in group.iterrows():
				feats_str = row['id'] + gf_str
				if row['__src__'] == '__tr__':
					f_tr.write(feats_str+'\n')
				elif row['__src__'] == '__va__':
					f_va.write(feats_str+'\n')

def cat(combined, names):
	if os.path.exists(combined):
		os.remove(combined)
	for name in names: 
		cmd = 'cat {0} >> {1}'.format(name, combined)
		p = subprocess.Popen(cmd, shell=True)
		p.communicate()


def delete(names):
	for name in names:
		cmd = 'rm {0}'.format(name)
		p = subprocess.Popen(cmd, shell=True)
		p.communicate()

def get_pid_table(df, col, sz_chunk):
	return df.groupby(col)['id'].count().cumsum().apply(lambda x: int(x/sz_chunk))

if __name__ == '__main__':
	args = parse_args()
	spec = '.T_{max_occur}.gins_{max_sz_group}.gfeat_{max_nr_group_feats}.gby_{g_field}.add_{a_field}'.format(
		max_occur=args['max_occur'], max_sz_group=args['max_sz_group'], max_nr_group_feats=args['max_nr_group_feats'],
		g_field=args['g_field'], a_field=args['a_field'])
	# loading
	start = time.time()
	tr = pd.read_csv(args['train'], dtype=str)
	tr['__src__'] = '__tr__'
	va = pd.read_csv(args['valid'], dtype=str)
	va['__src__'] = '__va__'
	trva = pd.concat([tr, va])
	if args['g_field'] != 'device_id':
		trva['__kid__'] = trva.apply(lambda row: '-'.join([row[c] for c in args['g_field'].split(',')]), axis=1)
	else:
		trva['__kid__'] = trva.apply(lambda row: row['device_id'] if row['device_id'] != 'a99f214a' else row['device_ip']+'-'+row['device_model'], axis=1)
	del tr
	del va
	print('Loading: {0} sec.'.format(time.time()-start))

	# assign process IDs
	start = time.time()
	sz_chunk = max(20000, int(len(trva)/100) + 1)
	trva['__pid__'] = get_pid_table(trva, '__kid__', sz_chunk)[trva['__kid__']].values
	pids = set(trva['__pid__'])
	tr_files = [args['train']+'.__tmp__.'+str(k)+spec for k in pids]
	va_files = [args['valid']+'.__tmp__.'+str(k)+spec for k in pids]
	print('Compute the sizes of groups: {0} sec.'.format(time.time()-start))

	# compute group features in parallel
	start = time.time()
	nr_procs = multiprocessing.cpu_count()
	pool = Pool(processes=nr_procs)

	result = pool.starmap(generate_feats, [(g[1], args['partition'], args['a_field'], args['gc_begin'], args['max_occur'], args['max_sz_group'], args['max_nr_group_feats'], f_tr, f_va) for g, f_tr, f_va in zip(trva.groupby('__pid__'), tr_files, va_files)])
	pool.close()
	pool.join()
	print('Calculate groups'' features: {0} sec.'.format(time.time()-start))

	# combine results and delete redundant files
	start = time.time()
	tr_path = args['train']+'.group'
	va_path = args['valid']+'.group'
	cat(tr_path, tr_files)
	cat(va_path, va_files)
	delete(tr_files)
	delete(va_files)
	print('Clean temporary files: {0} sec.'.format(time.time()-start))
