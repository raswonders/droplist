#!/usr/bin/env python3

import sys
import os.path

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
func_stats = {}

for x in lines:
  func = ' '.join(x.split()[3:])
  drops = int(x.split()[0])  
  if func in func_stats:
    func_stats[func] += drops
  else:
    func_stats[func] = drops

