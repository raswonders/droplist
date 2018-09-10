#!/usr/bin/env python3

import sys
import os.path

from collections import OrderedDict

def usage():
  print("Usage: droplist {filepath}")

def error1():
  print("Error: file \'{}\' doesn't exist".format(filename)) 


if len(sys.argv) == 1:
  usage()
  sys.exit(1)

filename = sys.argv[1]

if not os.path.exists(filename):
  error1()
  usage()
  sys.exit(1)

fh = open(filename, "r")
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




