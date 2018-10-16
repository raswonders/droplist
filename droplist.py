#!/usr/bin/env python3

"""
Droplist is parser for dropwatch output files  

Copyright (C) 2018 Rastislav Hepner

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os.path
import argparse
import re

from collections import OrderedDict

class TimeSignature(Exception):
  pass

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

def time_signature(lines):
  pattern = re.compile('\d+$')
  start = pattern.match(lines[0])
  if start:
    end = pattern.match(lines[-1])
    if end:
      start_time = int(end.group())
      end_time = int(start.group())
      elapsed_time = end_time - start_time 
      if elapsed_time > 0:
        return (start_time, end_time, elapsed_time)
  raise TimeSignature 

def drop_stats(lines):
  func_stats = {'ALL' : 0}
  """
  match groups of interest from pattern
  group(1) drops e.g. "233"
  group(3) function name with byte offset e.g. "skb_release_data+9a"
  group(4) byte offset for instance e.g. "+9e"
  group(5) memory address of a function e.g. "0xffffffff819ac3ca"
  """
  pattern = re.compile('(\d+)( drops at )(\w+(\+\w+)*) \((0x\w+)\)') 
  for x in lines:
    m = pattern.match(x)
    if m:
      func = m.group(3) 
      drops = int(m.group(1))  
      func_stats['ALL'] += drops
      if func in func_stats:
        func_stats[func] += drops
      else:
        func_stats[func] = drops
  return OrderedDict(sorted(func_stats.items(), key=lambda t: t[1], reverse=True))

def parse_dropwatch(fh):
  lines = fh.readlines()
  try:
    time_sign = time_signature(lines)
  except TimeSignature:
    # without time info
    return drop_stats(lines)
  # with time info
  return drop_stats(lines, time_sign)

def main():
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("filename", help="dropwatch output file",
                      type=lambda x: open_file(parser, x))
  args = parser.parse_args()
  list_func(parse_dropwatch(args.filename))

if __name__ == "__main__":
  main()


