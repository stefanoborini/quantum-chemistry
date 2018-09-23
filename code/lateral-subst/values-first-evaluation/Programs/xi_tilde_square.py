import sys
import csv

import numpy

if len(sys.argv) < 1:
    print "Usage: "+sys.argv[0]+" bond_center_distance_file.csv"
    sys.exit(1)

f=file(sys.argv[1],"r")
values = numpy.array(numpy.array([float(x) for x in f]))
values_reversed = numpy.array(list(reversed(values)))

for v in values*values_reversed:
    print v

