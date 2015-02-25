#!/usr/bin/env python3

import argparse, csv, sys, pickle, collections, math

from common import *

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('tr_src_path', type=str)
parser.add_argument('va_src_path', type=str)
parser.add_argument('tr_dst_path', type=str)
parser.add_argument('va_dst_path', type=str)
args = vars(parser.parse_args())

fields = ['pub_id','pub_domain','pub_category','banner_pos','device_model','device_conn_type','C14','C17','C20','C21']

def convert(src_path, dst_path, is_train):
    with open(dst_path, 'w') as f:
        for row in csv.DictReader(open(src_path)):
            i = 1
            w = math.sqrt(2)/math.sqrt(15)
            feats = []

            for field in fields:
                v = hashstr(field+'-'+row[field])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
                i += 1

            v = hashstr('hour-'+row['hour'][-2:])
            feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            i += 1

            if int(row['device_ip_count']) > 1000:
                v = hashstr('device_ip-'+row['device_ip'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            else:
                v = hashstr('device_ip-less-'+row['device_ip_count'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            i += 1

            if int(row['device_id_count']) > 1000:
                v = hashstr('device_id-'+row['device_id'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            else:
                v = hashstr('device_id-less-'+row['device_id_count'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            i += 1

            if int(row['smooth_user_hour_count']) > 30:
                v = hashstr('smooth_user_hour_count-0')
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            else:
                v = hashstr('smooth_user_hour_count-'+row['smooth_user_hour_count'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            i += 1

            if int(row['user_count']) > 30:
                v = hashstr('user_click_histroy-'+row['user_count'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            else:
                v = hashstr('user_click_histroy-'+row['user_count']+'-'+row['user_click_histroy'])
                feats.append('{i}:{v}:{w:.20f}'.format(i=i, v=v, w=w))
            i += 1

            f.write('{0} {1} {2}\n'.format(row['id'], row['click'], ' '.join(feats)))

convert(args['tr_src_path'], args['tr_dst_path'], True)
convert(args['va_src_path'], args['va_dst_path'], False)
