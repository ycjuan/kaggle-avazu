#!/usr/bin/env python3

import argparse, csv, sys, pickle, collections, time

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('tr_src_path', type=str)
parser.add_argument('va_src_path', type=str)
parser.add_argument('tr_app_dst_path', type=str)
parser.add_argument('va_app_dst_path', type=str)
parser.add_argument('tr_site_dst_path', type=str)
parser.add_argument('va_site_dst_path', type=str)
args = vars(parser.parse_args())

FIELDS = ['id','click','hour','banner_pos','device_id','device_ip','device_model','device_conn_type','C14','C17','C20','C21']
NEW_FIELDS = FIELDS+['pub_id','pub_domain','pub_category','device_id_count','device_ip_count','user_count','smooth_user_hour_count','user_click_histroy']

id_cnt = collections.defaultdict(int)
ip_cnt = collections.defaultdict(int)
user_cnt = collections.defaultdict(int)
user_hour_cnt = collections.defaultdict(int)

start = time.time()

def scan(path):
    for i, row in enumerate(csv.DictReader(open(path)), start=1):
        if i % 1000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))

        user = def_user(row)
        id_cnt[row['device_id']] += 1
        ip_cnt[row['device_ip']] += 1
        user_cnt[user] += 1
        user_hour_cnt[user+'-'+row['hour']] += 1

history = collections.defaultdict(lambda: {'history': '', 'buffer': '', 'prev_hour': ''})

def gen_data(src_path, dst_app_path, dst_site_path, is_train):
    reader = csv.DictReader(open(src_path))
    writer_app = csv.DictWriter(open(dst_app_path, 'w'), NEW_FIELDS)
    writer_site = csv.DictWriter(open(dst_site_path, 'w'), NEW_FIELDS)
    writer_app.writeheader()
    writer_site.writeheader()

    for i, row in enumerate(reader, start=1):
        if i % 1000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))
        
        new_row = {}
        for field in FIELDS:
            new_row[field] = row[field]

        new_row['device_id_count'] = id_cnt[row['device_id']]
        new_row['device_ip_count'] = ip_cnt[row['device_ip']]

        user, hour = def_user(row), row['hour']
        new_row['user_count'] = user_cnt[user]
        new_row['smooth_user_hour_count'] = str(user_hour_cnt[user+'-'+hour])

        if has_id_info(row):

            if history[user]['prev_hour'] != row['hour']:
                history[user]['history'] = (history[user]['history'] + history[user]['buffer'])[-4:]
                history[user]['buffer'] = ''
                history[user]['prev_hour'] = row['hour']

            new_row['user_click_histroy'] = history[user]['history']

            if is_train:
                history[user]['buffer'] += row['click']
        else:
            new_row['user_click_histroy'] = ''

        if is_app(row):
            new_row['pub_id'] = row['app_id']
            new_row['pub_domain'] = row['app_domain']
            new_row['pub_category'] = row['app_category']
            writer_app.writerow(new_row)
        else:
            new_row['pub_id'] = row['site_id']
            new_row['pub_domain'] = row['site_domain']
            new_row['pub_category'] = row['site_category']
            writer_site.writerow(new_row)

scan(args['tr_src_path'])
scan(args['va_src_path'])

print('======================scan complete======================')

gen_data(args['tr_src_path'], args['tr_app_dst_path'], args['tr_site_dst_path'], True)
gen_data(args['va_src_path'], args['va_app_dst_path'], args['va_site_dst_path'], False)
