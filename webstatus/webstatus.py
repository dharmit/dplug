#!/usr/bin/env python3

import argparse
import requests


def webstatus(filename):
    with open(filename) as f:
        content = f.readlines()

    for i in content:
        try:
            # setting timeout to avoid script from running forever till one
            # hits <Ctrl+C>.
            requests.get(i.strip('\n'), timeout=1)
            print ("Pass, {}".format(i.strip('\n')))
        except:
            print ("Error, {}".format(i.strip('\n')))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file containing websites.")
    args = parser.parse_args()

    webstatus(args.filename)

if __name__ == "__main__":
    parse()
