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

def find_func(l, r, sorted_dict):
  step_percent = 5
  ld = [] 
  i_k_l_combinations = [] 
  # How fast interval grows
  step = (float(l) * step_percent) / 100
  within_range = False
  jump = 0
  autosearch = False
  for i in range(21):
    if i == 1:
      if r == l and not within_range:
        print("No function or combination of them with drop count {} has been found.".format(drops)) 
        ans = input("Do you want to continue with autosearch? [Y]/N: ")
        if ans == 'y' or ans == 'Y' or not ans:
          autosearch = True
        else:
          break
      elif r == l and within_range:
        break
    if autosearch and within_range:
      break
    i_k_l_combinations.append([])
    rside = r + round(i * step) 
    lside = l - round(i * step)
    if lside < 0:
      lside = 0
    d = OrderedDict()
    # Build dictionary with functions which value <= right side of interval 
    for key,val in sorted_dict.items():
      if val <= rside:
        d[key] = val
    ld.append(d)
    if i > 0:
      # Build dictionary with just functions which were newly added this round
      d = { k : d[k] for k in set(d) - set(ld[i-1])}  
      new = len(d.keys())
      if not d:
        # if there are no newly added functions remember iteration i and repeat  
        if not jump:
          jump = i
        continue
    # If we skipped some iterations of i without saving combinations, correct references 
    if jump:
      i_correct = jump
      jump = 0
    else:
      i_correct = i
    for k in range(1, len(ld[i].keys()) + 1):
      l_combinations = list(itertools.combinations(ld[i].keys(), k)) 
      i_k_l_combinations[i].append(l_combinations)
      if i > 0:
        # Optimization skip combinations which were already computed  
        if k <= len(ld[i].keys()) - new:
          l_combinations = [ x for x in set(l_combinations) - set(i_k_l_combinations[i_correct-1][k-1])] 
      d_combinations = {key: compute_drops(key, ld[i]) for key in l_combinations}    
      for k,v in d_combinations.items():
        if lside <= v <= rside:
          list_func_comb(k, ld[i], v)
          within_range = True

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
  rside = drops + precision
  lside = drops - precision 
  if lside < 0:
    lside = 0
  find_func(lside, rside, func_stats_sorted)


