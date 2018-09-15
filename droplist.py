#!/usr/bin/env python3

import sys
import os.path
import argparse
import re

from collections import OrderedDict

def list_func(fn):
  print("{:^15s}|{:^65}".format("Drops", "Function"))
  print("-" * 80)
  for k in fn:
    v = func_stats_sorted[k]
    print("{:<15d}{:65s}".format(v, k))

def open_file(parser, fn):
  try:
    return open(fn, "r")
  except FileNotFoundError:
    parser.error("File \'{}\' doesn't exist".format(fn))

def parse_drops(parser, drops):
  pattern = re.compile(r'(\d+)(:(\d+)(%)?)?$')    
  m = pattern.match(drops)
  if m == None:
    # pattern wasn't matched
    parser.error("Invalid value for drops")
  elif m.group(2) == None:
    # drop count without precision 
    precision = 0
  elif m.group(4) == '%':
    # drop count with precision as percentage
    if int(m.group(3)) > 100:
      parser.error("Precision cannot be higher than 100%")
    precision = int(round(float(m.group(3)) * float(m.group(1))  / 100)) 
  else:
    # drop count with precision as whole number 
    precision = int(m.group(3))
  drops = int(m.group(1))
  return (drops, precision)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="dropwatch output file",
                    type=lambda x: open_file(parser, x))
parser.add_argument("-d", "--drops", help="[d[:p]] d number of drops you're searching for, p is allowed deviation from drop count. Deviation can be expressed either in percentage or as a whole number",
                    type=lambda x: parse_drops(parser, x))
args = parser.parse_args()

# Process dropwatch output file
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

if args.drops != None:
  rside = drops + precision
  lside = drops - precision 
  if lside < 0:
    lside = 0


