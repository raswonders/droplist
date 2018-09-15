#!/usr/bin/env python3

import sys
import os.path
import argparse
import re
import itertools

from collections import OrderedDict

def list_func(f_list, f_dict):
  print("{:^15s}|{:^65}".format("Drops", "Function"))
  print("-" * 80)
  if f_list:
    for k in f_list:
      v = f_dict[k]
      print("{:<15d}{:65s}".format(v, k))
  else:
    for k,v in f_dict.items():
      print("{:<15d}{:65s}".format(v, k))

def list_func_comb(iterator, f_dict, total):
  k = len(iterator)
  if k == 1: 
    print("{:^15s}|{:^65}".format("Drops", "Function"))
    print("-" * 80)
    print("{:<15d}{:65s}".format(f_dict[iterator[0]], iterator[0]))
  elif k > 1:
    title = str(k) + "-combination of functions"
    print("{:^15s}|{:^65}".format("Drops", title))
    print("-" * 80)
    for func in iterator:
      print("{:<15d}{:65s}".format(f_dict[func], func))
    print("{:<15d}{:65s}".format(total, "TOTAL"))

    


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

def compute_drops(iterator, f_dict):
  drops = 0
  for i in iterator:
    drops += f_dict[i]
  return drops

def find_func(drops, precision, sorted_dict):
  rside = drops + precision
  lside = drops - precision 
  if lside < 0:
    lside = 0
  d = OrderedDict()
  for key,val in sorted_dict.items():
    if val <= rside:
      d[key] = val
  #for k in range(1, len(d) + 1):
  for k in range(1, 3):
    l_combinations = list(itertools.combinations(d.keys(), k)) 
    d_combinations = {key: compute_drops(key, d) for key in l_combinations}    
    for k,v in d_combinations.items():
      if lside <= v <= rside:
        list_func_comb(k, d, v)
  #list_func(None, d)   
    
  




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
  drops = args.drops[0]
  precision = args.drops[1]
  find_func(drops, precision, func_stats_sorted)


