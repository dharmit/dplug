#!/usr/bin/env python3

import os
import sys 
import zipfile 
import argparse 
import zlib
 
def source_exists(source):
    if os.path.exists(source):
        return True
    return False

def zippy(source, destination = None):
    if not source_exists(source):
        print ("{} does not exist.".format(source))
        sys.exit(1)
    if os.path.isdir(source):
        with zipfile.ZipFile(destination, 'w') as zf: 
            for root, dirs, files in os.walk(source):
                for fil in files:
                    if fil[0] != '.':
                        zf.write(os.path.join(root, fil), compress_type =
                                zipfile.ZIP_DEFLATED)
        print ("Done")
    else:
        with zipfile.ZipFile(destination, 'w') as zf:
            zf.write(source, compress_type = zipfile.ZIP_DEFLATED)
        print ("Done")


def parse():
    parser = argparse.ArgumentParser(description = "Create zip files")
    parser.add_argument("source", help = "file or directory to be zipped")
    parser.add_argument("destination", help = 'destination of the zip file')
    args = parser.parse_args()
    zippy(args.source, args.destination)

if __name__ == "__main__":
    parse()
