#/usr/bin/env python
# @author Stefano Borini
# @description performs coumulative operations of the values along a column
# @license Artistic License 2.0

import os
import sys
import getopt
import math
import csv

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(1,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

import numpy

class Options:
    DEFAULT_SEPARATOR = ","
    def __init__(self): # fold>>
        self.input_filename = None
        self.separator = None
        self.operation = None 
    # <<fold

def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "s:o:h", ["separator=","operation=","help"])

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)

        if opt[0] == "-s" or opt[0] == "--separator":
            options.separator=opt[1]
        if opt[0] == "-o" or opt[0] == "--operation":
            options.operation = opt[1].split(",")
            
    if options.operation is None:
        _usage()
        sys.exit(1)
        
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
    print "Performs transformation on specific columns."
    print ""
    print "--separator=character"
    print "         change the separator (default comma ,)"
    print "--operation=column,operation"
    print "         perform the specific operation on a given column number (1-based)"
    print "         operation is a conventional string. Currently supported are sum, avg, min, max"
# <<fold

class Dialect(csv.Dialect):
    def __init__(self, delimiter):
        self.delimiter = delimiter
        self.doublequote = True
        self.lineterminator = '\n'
        self.quotechar = '"'
        self.quoting = 0
        self.skipinitialspace = False

def main(argv): # fold>>

    options = _getOptions(argv)
    if options.input_filename is not None:
        f=file(options.input_filename)
    else:
        f=sys.stdin
    
    csv.register_dialect("mydialect", Dialect(options.separator))
    csvreader = csv.reader(f, dialect="mydialect")

    l = []
    for row in csvreader:
        if row[0].strip()[0] == "#" or len(row) == 0:
            continue
        l.append(float(row[int(options.operation[0])-1]))
   
    a = numpy.array(l)
    if options.operation[1] == "sum":
        print numpy.sum(a)
    elif options.operation[1] == "avg":
        print numpy.average(a)
    elif options.operation[1] == "max":
        print numpy.max(a)
    elif options.operation[1] == "min":
        print numpy.min(a)
    else:
        raise Exception("Unimplemented operation")
    # <<fold


if __name__ == "__main__":
    main(sys.argv)



