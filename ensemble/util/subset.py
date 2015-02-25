#!/usr/bin/env python3

import argparse, csv, sys, time, collections

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('filter_string', type=str)
parser.add_argument('tr_src_path', type=str)
parser.add_argument('va_src_path', type=str)
parser.add_argument('tr_dst_path', type=str)
parser.add_argument('va_dst_path', type=str)
args = vars(parser.parse_args())

filter = collections.defaultdict(list) 
inv_filter = collections.defaultdict(list)
cnt_filter = collections.defaultdict(list)
inv_end_filter = collections.defaultdict(list)
cold_user_filter = False
for token in args['filter_string'].split(','):
    if token.startswith('D'):
        cold_user_filter = True
    else:
        type, field, value = token.split('-')
        if type == 'A':
            filter[field].append(value)
        elif type == 'B':
            inv_filter[field].append(value)
        elif type == 'C':
            cnt_filter[field].append(int(value))
        elif type == 'E':
            inv_end_filter[field].append(value)
        else:
            print('unknown filter type')
            exit(1)

start = time.time()

cnt = collections.defaultdict(int)

def scan(path):
    for i, row in enumerate(csv.DictReader(open(path)), start=1):
        if i % 10000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))

        for field in cnt_filter:
            cnt[field+'-'+row[field]] += 1

user_set = set()
def scan_user(path):
    for i, row in enumerate(csv.DictReader(open(path)), start=1):
        if i % 10000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))

        user_set.add(def_user(row))

def subset(src_path, dst_path, is_train):
    reader = csv.DictReader(open(src_path))
    writer = csv.DictWriter(open(dst_path, 'w'), reader.fieldnames)
    writer.writeheader()

    for i, row in enumerate(reader, start=1):
        if i % 10000000 == 0:
            sys.stderr.write('{0:6.0f}    {1}m\n'.format(time.time()-start,int(i/1000000)))

        match = True
        for field, values in filter.items():
            for value in values:
                if not row[field].startswith(value):
                    match = False
                    break
        if not match:
            continue
        
        for field, values in inv_end_filter.items():
            for value in values:
                if row[field].endswith(value):
                    match = False
                    break
        if not match:
            continue
        
        for field, values in cnt_filter.items():
            for value in values:
                if cnt[field+'-'+row[field]] != value:
                    match = False
                    break
        if not match:
            continue

        for field, values in inv_filter.items():
            for value in values:
                if row[field].startswith(value):
                    match = False
                    break
        if not match:
            continue

        if cold_user_filter and not is_train:
            user = def_user(row)
            if user not in user_set:
                match = False
        if not match:
            continue

        writer.writerow(row)

if len(cnt_filter) != 0:
    print('=====scanning=====')
    scan(args['tr_src_path'])
    scan(args['va_src_path'])

if cold_user_filter:
    print('=====scanning=====')
    scan_user(args['tr_src_path'])

print('=====subsetting=====')
subset(args['tr_src_path'], args['tr_dst_path'], True)
subset(args['va_src_path'], args['va_dst_path'], False)
