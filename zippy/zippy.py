#!/usr/bin/env python3

import os
import sys 
import zipfile 
import argparse 
import zlib
 
def source_exists(source):
    """
    This function checks if the file/directory specified by the user exists or
    not.
    """
    if os.path.exists(source):
        return True
    return False

def source_is_dir(source):
    """
    This function checks if the source provided by the user is a directory.
    """
    if os.path.isdir(source):
        return True
    return False

def zip_dir(source, destination):
    """
    This function is used to zip a directory specified by the user.
    """
    try:
        zf = zipfile.ZipFile(destination, 'w')
        for root, dirs, files in os.walk(source):
            for fil in files:
                if fil[0] != '.':
                    print (fil)
                    zf.write(os.path.join(root, fil))
    finally:
        zf.close()
        print ("Done")

def zip_file(source, destination):
    """
    This function is used to zip a file specified by the user.
    """
    with zipfile.ZipFile(destination, 'w') as zf:
        zf.write(source, compress_type = zipfile.ZIP_DEFLATED)
        print ("Done")

def zippy(source, destination = None):
    """
    This function first checks if the source file/directory exists. Next, it
    checks if the source is a directoy. If it is, it calls the function zip_dir
    else it called zip_file.
    """
    if not source_exists(source):
        print ("{} does not exist.".format(source))
        sys.exit(1)
    if source_is_dir(source):
        zip_dir(source, destination)
    else:
        zip_file(source, destination)

def parse():
    """
    This is the main parsing function being used.
    """
    # Create a parser
    parser = argparse.ArgumentParser(description = "Create zip files")

    # Add arguments to the parser
    parser.add_argument("source", help = "file or directory to be zipped")
    parser.add_argument("destination", help = 'destination of the zip file')
    parser.add_argument("-f", "--force", help = "Overwrite existing zip file \
            (if any)", action = "store_true")
    args = parser.parse_args()

    # Check if the zip file already exists and present relevant options or
    # create a zip file if none already exists with same name as that provided
    # as destination.

    if args.force:
        zippy(args.source, args.destination)
    elif os.path.exists(args.destination):
        choice = input("{} already exists. Do you want to overwrite? "
                       "(y/n)? ".format(args.destination))
        if choice == 'y':
            if os.remove(args.destination):
                print ("removed!!!!")
            else:
                print ("Not remove!!!!!! ")
            zippy(args.source, args.destination)
        elif choice == 'n':
            print ("Try another name")
            sys.exit(1)
        else:
            print ("Invalid choice. Either use -f to overwrite {} or choose "
                   "different name".format(args.destination))
            sys.exit(1)
    else:
        zippy(args.source, args.destination)

if __name__ == "__main__":
    parse()
