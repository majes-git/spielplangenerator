#!/usr/bin/env python

from __future__ import print_function
import json
import os
import sys


def usage():
    print("Usage: {} <config file>".format(sys.argv[0]))
    sys.exit(1)


def load_config(filename):
    dirpath = os.path.dirname(sys.argv[0])
    config_file = sys.argv[1]
    if filename == os.path.isabs(filename):
        abs_filename = filename
    else:
        abs_filename = os.path.join(dirpath, filename)
    try:
        config = json.load(open(abs_filename))
    except:
        print("Could not load config file!")
        usage()
    return config
