#/usr/bin/env python
# @author Stefano Borini
# @description performs linear regression on a given dataset
# @license Artistic License 2.0

import os
import sys
import getopt

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

import numpy
from scipy import stats

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
    print "calculates linear regression of the data in a csv file. The first column is used as x."
    print "The second column is used as y."
    print "the result is returned as a comma separated set of values:"
    print ""
    print "slope, intercept, r, two-tailed prob, stderr-of-the-estimate"
    print ""
    print "--separator=character"
    print "         change the separator (default comma ,)"
#    print "--x-column=number"
#    print "--y-column=number"
#    print "         use different columns for x and y. number is 1-based (first column is 1, etc...)"
#    print "         if not specified, the first two columns are used by default. If the file contains"
#    print "         only one column, this column is used as y, and x is a progressive incremental number"
#    print "         starting from zero"
# <<fold

def main(argv): # fold>>

    options = _getOptions(argv)
    if options.input_filename is not None:
        f=file(options.input_filename)
    else:
        f=sys.stdin
    lines = [line for line in f.readlines() if len(line.strip()) != 0 and line.strip()[0] != "#" and line.strip()[0] != "\n" ]
    f.close()

    x=numpy.array([float(qq.split(options.separator)[0]) for qq in lines])
    y=numpy.array([float(qq.split(options.separator)[1]) for qq in lines])

    print "# linreg results"
    print "# slope, intercept, r, two-tailed prob, stderr-of-the-estimate"
    print "%f, %f, %f, %f, %f\n" % stats.linregress(x,y)

    # <<fold


if __name__ == "__main__":
    main(sys.argv)



