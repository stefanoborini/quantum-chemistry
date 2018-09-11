#/usr/bin/env python
# @author Stefano Borini
# @description performs linear regression on a given dataset
# @license Artistic License 2.0

import os
import sys
import getopt
import math
import csv

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

class Options:
    DEFAULT_SEPARATOR = ","
    def __init__(self): # fold>>
        self.input_filename = None
        self.separator = None
    # <<fold

def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "s:h", ["separator=","help"])

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)

        if opt[0] == "-s" or opt[0] == "--separator":
            options.separator=opt[1]

    if options.separator is None:
        options.separator = Options.DEFAULT_SEPARATOR

    if len(args) != 1:
        options.input_filename = None
    else:
        options.input_filename = args[0]
    return options
    # <<fold

def _usage(): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" input"
    print ""
    print "Transpose a csv file"
    print ""
    print "--separator=character"
    print "         change the separator (default comma ,)"
# <<fold

def main(argv): # fold>>

    options = _getOptions(argv)
    if options.input_filename is not None:
        f=file(options.input_filename)
    else:
        f=sys.stdin

    csv_reader = csv.reader(f, dialect='excel')
    
    rows=[]
    for row in csv_reader:
        rows.append(row)

    csv_writer = csv.writer(sys.stdout, dialect="excel")
    for row in zip(*rows):
        csv_writer.writerow(row)



if __name__ == "__main__":
    main(sys.argv)



