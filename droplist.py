#!/usr/bin/env python3

import sys
import os.path

from collections import OrderedDict
from argparse import ArgumentParser

def file_error(fn):
  print("Error: file \'{}\' doesn't exist".format(fn)) 

parser = ArgumentParser()
parser.add_argument("filename", help="dropwatch output file")
args = parser.parse_args()

if not os.path.exists(args.filename):
  file_error(args.filename)
  parser.print_help()
  sys.exit(1)

fh = open(args.filename, "r")
lines = fh.readlines()
func_stats = {'TOTAL' : 0}

for x in lines:
  func = ' '.join(x.split()[3:])
  drops = int(x.split()[0])  
  func_stats['TOTAL'] += drops
  if func in func_stats:
    func_stats[func] += drops
  else:
    func_stats[func] = drops

func_stats_sorted = OrderedDict(sorted(func_stats.items(), key=lambda t: t[1], reverse=True))

print("{:^15s}|{:^65}".format("Drops", "Function"))
print("-" * 80)
for k, v in func_stats_sorted.items():
  print("{:<15d}{:65s}".format(v, k))




