#!/usr/bin/env python
# @author: Stefano Borini

import sys
import parameters

try:
    number_of_double_bonds=int(sys.argv[1])
    if number_of_double_bonds < 2:
        raise Exception()
except:
    print "Usage : "+sys.argv[0]+" repetitions"
    print """
Script that generates polyacetylenes in a format suitable for the script zmat2input in
TheoChemPy. The number of repetition is the amount of repetitions of the central H-C=C-H
unit.
"""
    sys.exit(1)


print "[parameters]"
print parameters.parameters()
print """[zmatrix distance_unit="Angstrom" angle_unit="degrees"]
H 1 
X 2 1 rch 
C 3 1 rch 2 120. 
H 4 3 rch 1 120. 2 180.0
C 5 3 rc2 1 120. 2 0.0
H 6 5 rch 3 120. 4 180.0"""

number_of_units = number_of_double_bonds-2
for i in xrange (0,number_of_units):
    print "C "+str(7+i*4)+" "+str(5+i*4)+" rc1 "+str(6+i*4)+" 120. "+str(3+i*4)+" 180.0"
    print "H "+str(8+i*4)+" "+str(7+i*4)+" rch "+str(5+i*4)+" 120. "+str(6+i*4)+" 180.0"
    print "C "+str(9+i*4)+" "+str(7+i*4)+" rc2 "+str(5+i*4)+" 120. "+str(3+i*4)+" 180.0"
    print "H "+str(10+i*4)+" "+str(9+i*4)+" rch "+str(7+i*4)+" 120. "+str(8+i*4)+" 180.0"

print "C "+str(7+number_of_units*4)+" "+str(5+number_of_units*4)+" rc1 "+str(6+number_of_units*4)+" 120. "+str(3+number_of_units*4)+" 180.0"
print "H "+str(8+number_of_units*4)+" "+str(7+number_of_units*4)+" rch "+str(5+number_of_units*4)+" 120. "+str(6+number_of_units*4)+" 180.0"
print "C "+str(9+number_of_units*4)+" "+str(7+number_of_units*4)+" rc2 "+str(5+number_of_units*4)+" 120. "+str(3+number_of_units*4)+" 180.0"
print "H "+str(10+number_of_units*4)+" "+str(9+number_of_units*4)+" rch "+str(7+number_of_units*4)+" 120. "+str(8+number_of_units*4)+" 180.0"

print "N "+str(11+number_of_units*4)+" "+str(9+number_of_units*4)+" rcnh2 "+str(7+number_of_units*4)+" 120. "+str(8+number_of_units*4)+" 0.0"
print "H "+str(12+number_of_units*4)+" "+str(11+number_of_units*4)+" rnh "+str(9+number_of_units*4)+" 120. "+str(7+number_of_units*4)+" 0.0"
print "H "+str(13+number_of_units*4)+" "+str(11+number_of_units*4)+" rnh "+str(9+number_of_units*4)+" 120. "+str(7+number_of_units*4)+" 180.0"
print """[basis]
* 6-31G*
[symmetry]
X
"""
