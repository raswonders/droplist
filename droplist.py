#!/usr/bin/env python3

import sys
import os.path
import argparse

from collections import OrderedDict

def list_func(f_dict):
  print("{:^15s}|{:^65}".format("Drops", "Function"))
  print("-" * 80)
  for k,v in f_dict.items():
    print("{:<15d}{:65s}".format(v, k))

def open_file(parser, fn):
  try:
    return open(fn, "r")
  except FileNotFoundError:
    parser.error("File \'{}\' doesn't exist".format(fn))

def compute_drops(iterator, f_dict):
  drops = 0
  for i in iterator:
    drops += f_dict[i]
  return drops

def parse_dropwatch(fh):
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
  return OrderedDict(sorted(func_stats.items(), key=lambda t: t[1], reverse=True))

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="dropwatch output file",
                    type=lambda x: open_file(parser, x))
args = parser.parse_args()
func_stats_sorted = parse_dropwatch(args.filename) 
list_func(func_stats_sorted)

