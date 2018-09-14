#!/usr/bin/env python3

import sys
import os.path
import argparse
import re

from collections import OrderedDict

def open_file(parser, fn):
  try:
    return open(fn, "r")
  except FileNotFoundError:
    parser.error("File \'{}\' doesn't exist".format(fn))

def parse_drops(parser, p, p_def):
  pattern = re.compile(r'(\d+)(:(\d+)(%)?)?$')    
  m = pattern.match(p)
  if m == None:
    # pattern wasn't matched
    parser.error("Invalid value for drops")
  elif m.group(2) == None:
    # drop count without precision 
    precision = int(round(float(p_def) * float(m.group(1)) / 100))
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

# Default precision in percentage  
p_def = 2
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="dropwatch output file",
                    type=lambda x: open_file(parser, x))
parser.add_argument("-d", "--drops", help="[d[:p]] d number of drops you're searching for, p is allowed deviation from drop count. Deviation can be expressed either in percentage or as a whole number",
                    type=lambda x: parse_drops(parser, x, p_def))
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

if args.drops != None:
  drops = int(args.drops[0])
  precision = int(args.drops[1])
  func_match_drops = [ k for k,v in func_stats_sorted.items() if v == drops ]
  if func_match_drops: 
    list_func(func_match_drops)
  elif precision == 0:
    print("Interested in closest match? [Y]/N")
    #TODO implement search within inflating drop range  
  else:
    rside = drops + precision
    lside = drops - precision 
    if lside < 0:
      lside = 0
    #TODO implement search within drop range lside - rside 
