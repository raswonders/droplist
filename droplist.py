#!/usr/bin/env python3

import sys
import os.path

def usage():
  print("Usage: droplist {filepath}")

if len(sys.argv) == 1:
  usage()
  sys.exit(1)

