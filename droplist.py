#!/usr/bin/env python3

import sys
import os.path
import argparse

from collections import OrderedDict

def open_file(parser, fn):
  try:
    return open(fn, "r")
  except FileNotFoundError:
    parser.error("File \'{}\' doesn't exist".format(fn))

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="dropwatch output file",
                    type=lambda x: open_file(parser, x))
parser.add_argument("-d", "--drops", help="amount of drops you're searching for",
                    type=int)
args = parser.parse_args()

fh = args.filename
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


