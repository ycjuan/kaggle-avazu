#!/usr/bin/env python3

import argparse, csv, sys, pickle, collections, time

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('tr_src_path', type=str)
parser.add_argument('va_src_path', type=str)
parser.add_argument('tr_dst_path', type=str)
parser.add_argument('va_dst_path', type=str)
args = vars(parser.parse_args())

SIMPLE_FIELDS = ['id','click','hour','banner_pos','device_id','device_ip','device_model','device_type','device_conn_type','C1','C14','C15','C16','C17','C18','C19','C20','C21']
NEW_FIELDS = SIMPLE_FIELDS + ['pub_id','pub_domain','pub_category','device_id_cnt','device_ip_cnt','user_cnt','user_hour_cnt','user_click_history','sp1_cnt','user_click_history2']

id_cnt = collections.defaultdict(int)
ip_cnt = collections.defaultdict(int)
user_cnt = collections.defaultdict(int)
user_hour_cnt = collections.defaultdict(int)
sp1_cnt = collections.defaultdict(int)

start = time.time()

def def_sp1(row):
    sp1 = ''
    for field in ['hour','banner_pos','device_id','device_ip','device_model','device_type','device_conn_type','C1','C14','C15','C16','C17','C18','C19','C20','C21','app_id','app_domain','app_category','site_id','site_domain','site_category']:
        sp1 += row[field]
    return sp1


def scan(path):
    for i, row in enumerate(csv.DictReader(open(path)), start=1):
        if i % 10000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))

        user, user_hour = def_user(row), def_user_hour(row)
        id_cnt[row['device_id']] += 1
        ip_cnt[row['device_ip']] += 1
        user_cnt[user] += 1
        user_hour_cnt[user_hour] += 1

        sp1_cnt[def_sp1(row)] += 1


history = collections.defaultdict(lambda: {'history': '', 'buffer': '', 'prev_hour': ''})
history2 = collections.defaultdict(lambda: {'history': '', 'buffer': '', 'prev_hour': ''})

def gen_data(src_path, dst_path, is_train):
    reader = csv.DictReader(open(src_path))
    writer = csv.DictWriter(open(dst_path, 'w'), NEW_FIELDS)
    writer.writeheader()

    for i, row in enumerate(reader, start=1):
        if i % 10000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))
        
        new_row = {}
        for field in SIMPLE_FIELDS:
            new_row[field] = row[field]

        new_row['device_id_cnt'] = id_cnt[row['device_id']]
        new_row['device_ip_cnt'] = ip_cnt[row['device_ip']]

        user, hour, user_hour = def_user(row), row['hour'], def_user_hour(row)
        new_row['user_cnt'] = user_cnt[user]
        new_row['user_hour_cnt'] = user_hour_cnt[user_hour]
        new_row['sp1_cnt'] = sp1_cnt[def_sp1(row)]

        if has_id_info(row):

            if history[user]['prev_hour'] != row['hour']:
                history[user]['history'] = (history[user]['history'] + history[user]['buffer'])[-4:]
                history[user]['buffer'] = ''
                history[user]['prev_hour'] = row['hour']

            new_row['user_click_history'] = history[user]['history']

            if is_train:
                history[user]['buffer'] += row['click']
        else:
            if history2[user]['prev_hour'] != row['hour']:
                history2[user]['history'] = (history2[user]['history'] + history2[user]['buffer'])[-4:]
                history2[user]['buffer'] = ''
                history2[user]['prev_hour'] = row['hour']

            new_row['user_click_history2'] = history2[user]['history']

            if is_train:
                history2[user]['buffer'] += row['click']

        if is_app(row):
            new_row['pub_id'] = row['app_id']
            new_row['pub_domain'] = row['app_domain']
            new_row['pub_category'] = row['app_category']
        else:
            new_row['pub_id'] = row['site_id']
            new_row['pub_domain'] = row['site_domain']
            new_row['pub_category'] = row['site_category']

        writer.writerow(new_row)

print('=====scanning=====')
scan(args['tr_src_path'])
scan(args['va_src_path'])

print('=====generating=====')
gen_data(args['tr_src_path'], args['tr_dst_path'], True)
gen_data(args['va_src_path'], args['va_dst_path'], False)
