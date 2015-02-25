#!/usr/bin/env python3

import argparse, sys, subprocess

if len(sys.argv) == 1:
    sys.argv.append('-h')

parser = argparse.ArgumentParser()
parser.add_argument('task_path', type=str)
args = vars(parser.parse_args())

tasks = []
for line in open(args['task_path']):
    log_path, cmd = line.strip().split(' ', 1)
    tasks.append({'log_path': log_path, 'cmd': cmd})

workers = []
for task in tasks:
    worker = subprocess.Popen(task['cmd'].split(), stdout=open(task['log_path'], 'w'))
    workers.append(worker)

for worker in workers:
    worker.communicate()
