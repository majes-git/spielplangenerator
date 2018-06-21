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

    print("Nr.;;;;Datum;;Uhrzeit;;Heim-Mannschaft;;Gast-Mannschaft;;;;")
    i = 0
    for spiel in schema:
        line = u"{};;;;{};;00:00;;{};;{};;;;".format(
            1 + i,
            spieltage[str(spiel[2])],
            teams[spiel[0] - 1][0],
            teams[spiel[1] - 1][0]
        )
        print(line.encode('windows-1252'))
        i += 1


if __name__ == '__main__':
    main()
