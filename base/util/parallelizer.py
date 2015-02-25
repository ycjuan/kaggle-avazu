#!/usr/bin/env python3

import argparse, sys

from common import *

def parse_args():
    
    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='nr_thread', default=12, type=int)
    parser.add_argument('cvt_path')
    parser.add_argument('tr_src_path')
    parser.add_argument('va_src_path')
    parser.add_argument('tr_dst_path')
    parser.add_argument('va_dst_path')
    args = vars(parser.parse_args())

    return args

def main():
    
    args = parse_args()

    nr_thread = args['nr_thread']
    
    split(args['tr_src_path'], nr_thread, True)
    split(args['va_src_path'], nr_thread, True)

    parallel_convert(args['cvt_path'], [args['tr_src_path'], args['va_src_path'], args['tr_dst_path'], args['va_dst_path']], nr_thread)

    delete(args['tr_src_path'], nr_thread)
    delete(args['va_src_path'], nr_thread)

    cat(args['tr_dst_path'], nr_thread)
    cat(args['va_dst_path'], nr_thread)

    delete(args['tr_dst_path'], nr_thread)
    delete(args['va_dst_path'], nr_thread)

main()
