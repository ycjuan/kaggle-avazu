#!/usr/bin/env python3

import argparse, csv, sys, pickle, collections, time

sys.path.append('util')

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('src_path', type=str)
parser.add_argument('dst_path', type=str)
args = vars(parser.parse_args())

fields = ['pub_id','pub_domain','pub_category','banner_pos','device_model','device_conn_type','C14','C17','C20','C21']

start = time.time()

def convert(src_path, dst_path, is_train):
    with open(dst_path, 'w') as f:
        for i, row in enumerate(csv.DictReader(open(src_path)), start=1):
            if i % 10000000 == 0:
                sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))
            
            feats = []

            for field in fields:
                feats.append(hashstr(field+'-'+row[field]))

            if int(row['device_ip_cnt']) > 20:
                feats.append(hashstr('device_ip-'+row['device_ip']))
            else:
                feats.append(hashstr('device_ip-less-'+row['device_ip_cnt']))

            feats.append(hashstr('bias'))

            if int(row['user_hour_cnt']) > 30:
                feats.append(hashstr('user_hour_cnt-0'))
            else:
                feats.append(hashstr('user_hour_cnt-'+row['user_hour_cnt']))

            if int(row['user_cnt']) > 30:
                feats.append(hashstr('user_click_history-'+row['user_cnt']))
            elif has_id_info(row):
                feats.append(hashstr('user_click_history-'+row['user_cnt']+'-'+row['user_click_history']))
            else:
                feats.append(hashstr('user_click_history2-'+row['user_cnt']+'-'+row['user_click_history2']))

            feats.append(hashstr('user_count-'+row['user_cnt']))

            f.write('{0} {1}\n'.format(row['click'], ' '.join(feats)))

print('=====converting=====')
convert(args['src_path'], args['dst_path'], True)
