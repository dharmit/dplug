#!env/bin/python

import argparse
import json
import os
import sys
from walkdir import filtered_walk, file_paths


# Tags to be set to the files.
# TAGS = {'c': ['c', 'cpp'],
#        'photos': ['jpg', 'jpeg', 'png'],
#        'vector': ['svg'],
#        'markup': ['html', 'css'],
#        'font': ['ttf'],
#        'javascript': ['js']
#        }

TAGS = {'c': 'c',
        'cpp': 'c',
        'js': 'javascript',
        'py': 'python',
        'svg': 'vector',
        'jpeg': 'photos',
        'jpg': 'photos',
        'png': 'photos',
        'ttf': 'font',
        'html': 'markup',
        'css': 'markup',
        'json': 'json'
        }


def search(path):
    """
    This method takes path to a directory as an argument and returns list of
    files under it in the format:
        filename: absolute path
    """
    EXCLUDED_DIRS = ['env',
                     'venv',
                     '.git'
                     ]
    EXCLUDED_FILES = ['.gitignore',
                      '*.pyc',
                      '*.out'
                      ]

    files = {}

    for i in file_paths(filtered_walk(path, excluded_dirs=EXCLUDED_DIRS,
                                      excluded_files=EXCLUDED_FILES)):
        files[os.path.basename(i)] = os.path.realpath(i)
    return files


def tagged(files):
    """
    This function takes in a dictionary of the format:
        files: absolute path of the file
    and generates a json of the format:
        tag{
            file1: absolutepath,
            file2: absolutepath
            }
    """
    tagged_files = {'javascript': {},
                    'python': {},
                    'markup': {},
                    'photos': {},
                    'vector': {},
                    'c': {},
                    'font': {},
                    'untagged': {},
                    'json': {}
                    }
    for f in files:
        if files[f].split('.')[-1] in TAGS:
            tag = TAGS[files[f].split('.')[-1]]
            tagged_files[tag][f] = files[f]
        else:
            tagged_files['untagged'][f] = files[f]

    return tagged_files


def search_and_tag(path):
    """
    This function will use two methods - i. search and ii. tag. One will use
    walkdir module to walk over the specified path and return a list of files
    under it and other will apply necessary tags to it.
    """
    # TODO - Make sure that only files with extensions are considered when
    # setting tags.
    files = search(path)
    tagged_files = tagged(files)
    with open('/tmp/tags.json', 'w') as f:
        f.write(json.dumps(tagged_files))

def check_dir_exists(path):
    if not os.path.isdir(path):
        return True
    return False


def create_parser():
    parser = argparse.ArgumentParser(description="Takes in the name of a"
                                     "directory and finds and tags all the"
                                     "files inside it.")
    parser.add_argument("path", help="path of the directory you want"
                        "to search over.")
    args = parser.parse_args()

    if not check_dir_exists(args.path):
        search_and_tag(args.path)
    else:
        print "{} is not a directory.".format(args.path)
        print "Make sure you provide absolute path."
        sys.exit(1)


if __name__ == "__main__":
    create_parser()
