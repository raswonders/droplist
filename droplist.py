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

