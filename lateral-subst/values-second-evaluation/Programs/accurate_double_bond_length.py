import sys
import math
import numpy

f=file(sys.argv[1])

for index, line in enumerate(f):
    if index % 2 == 0:
        first_atom = numpy.array(map(float,line.split(",")))
    else:
        second_atom = numpy.array(map(float,line.split(",")))
        distance = math.sqrt(numpy.dot(second_atom-first_atom, second_atom-first_atom))*0.5291772083 
        print distance
        second_atom = None
        first_atom = None
f.close()
        
