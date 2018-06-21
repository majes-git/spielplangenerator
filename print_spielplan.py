#!/usr/bin/env python

import json
import os
import sys


def load_config():
    dirpath = os.path.dirname(sys.argv[0])
    config_file = sys.argv[1]
    if config_file == os.path.isabs(config_file):
        filename = config_file
    else:
        filename = os.path.join(dirpath, config_file)
    try:
        config = json.load(open(filename))
    except Exception as e:
        print "Could not load config file: {}".format(e.message)
        print "Usage: {} <config file>".format(sys.argv[0])
        sys.exit(1)
    return config


def main():
    config = load_config()
    schema = json.load(open(config['schema']))
    spieltage = config['spieltage']
    teams = config['teams']

    i = 0
    for spiel in schema:
        line = "%s | %2s | %s | %-30s | %-30s" % (spieltage[str(spiel[2])], i / 3 + 1, teams[spiel[3] - 1][
            1], teams[spiel[0] - 1][0], teams[spiel[1] - 1][0])
        print line.encode('utf8')
        i += 1


if __name__ == '__main__':
    main()
