#!/usr/bin/env python

from __future__ import print_function
import json
import sys

from config import load_config, usage


def main():
    if len(sys.argv) != 2:
        usage()
    config_filename = sys.argv[1]
    config = load_config(config_filename)
    schema = json.load(open(config['schema']))
    spieltage = config['spieltage']
    teams = config['teams']

    i = 0
    for spiel in schema:
        line = "%s | %2s | %s | %-30s | %-30s" % (spieltage[str(spiel[2])], i / 3 + 1, teams[spiel[3] - 1][
            1], teams[spiel[0] - 1][0], teams[spiel[1] - 1][0])
        print(line.encode('utf8'))
        i += 1


if __name__ == '__main__':
    main()
