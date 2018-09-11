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

import numpy
from scipy import stats

class Options:
    DEFAULT_SEPARATOR = ","
    def __init__(self): # fold>>
        self.input_filename = None
        self.separator = None
        self.operations = []
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
            options.operations.append(opt[1].split(","))
            

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
    print "         operation is a conventional string. Currently supported are log, log10, neg, abs, pow2, sqrt"
    print "         multiple --operation options can be used. The execution is sequential, one after the"
    print "         other."
# <<fold

def main(argv): # fold>>

    options = _getOptions(argv)
    if options.input_filename is not None:
        f=file(options.input_filename)
    else:
        f=sys.stdin
    lines = [line for line in f.readlines() if len(line.strip()) != 0 and line.strip()[0] != "#" and line.strip()[0] != "\n" ]
    f.close()

    num_columns = len(lines[0].split(options.separator))
    arrays=[]

    for i in xrange(0,num_columns):
        arrays.append(numpy.array([float(qq.split(options.separator)[i]) for qq in lines]))
    arrays = applyFilters(arrays, options.operations)

    
    csv_writer = csv.writer(sys.stdout, dialect="excel")
    for row in zip(*arrays):
        csv_writer.writerow(row)


    # <<fold

def log10(value):
    return math.log(value, 10)

def neg(value):
    return -value

def pow2(value):
    return math.pow(value,2.0)

def sqrt(value):
    return math.sqrt(value)

def applyFilters(arrays, operations):
    def getFilter(string):
        if string == "log":
            return math.log
        elif string == "log10":
            return log10
        elif string == "neg":
            return neg
        elif string == "abs":
            return abs
        elif string == "pow2":
            return pow2
        elif string == "sqrt":
            return sqrt
        else:
            return None

    for column_string, operation_string in operations:
        operation = getFilter(operation_string)
        arrays_column = int(column_string)-1
        if operation is None:
            raise Exception("Unknown filter "+operation_string)

        arrays[arrays_column] = numpy.array(map(operation,arrays[arrays_column]))

    return arrays

if __name__ == "__main__":
    main(sys.argv)



