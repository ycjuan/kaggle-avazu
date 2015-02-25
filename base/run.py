#!/usr/bin/env python3

import subprocess, sys, os, time, socket

size = sys.argv[1]

start = time.time()
print('size = {size}'.format(size=size))

cmd = 'make -C mark/mark1 && ln -sf mark/mark1/mark1'
subprocess.call(cmd, shell=True)

cmd = './util/gen_data.py ../tr.r{size}.csv ../va.r{size}.csv tr.r{size}.app.new.csv va.r{size}.app.new.csv tr.r{size}.site.new.csv va.r{size}.site.new.csv'.format(size=size)
subprocess.call(cmd.split())

for category in ['app', 'site']:
    cmd = 'util/parallelizer.py -s 12 converter/2.py tr.r{size}.{category}.new.csv va.r{size}.{category}.new.csv tr.r{size}.{category}.sp va.r{size}.{category}.sp'.format(size=size, category=category)
    subprocess.call(cmd.split())

cmd = './mark1 -r 0.03 -s 1 -t 13 va.r{size}.app.sp tr.r{size}.app.sp'.format(size=size) 
subprocess.call(cmd.split())
cmd = './mark1 -r 0.03 -s 1 -t 17 va.r{size}.site.sp tr.r{size}.site.sp'.format(size=size) 
subprocess.call(cmd.split())

for category in ['app', 'site']:
    cmd = './util/pickle_prediction.py va.r{size}.{category}.sp.prd va.r{size}.{category}.sp.prd.pickle'.format(size=size, category=category) 
    subprocess.call(cmd.split())

cmd = './util/merge_prediction.py va.r{size}.app.sp.prd.pickle va.r{size}.site.sp.prd.pickle va.r{size}.prd.pickle'.format(size=size) 
subprocess.call(cmd.split())

cmd = './util/unpickle_prediction.py va.r{size}.prd.pickle base.r{size}.prd'.format(size=size)
subprocess.call(cmd.split())

print('time used = {0:.0f}'.format(time.time()-start))
