#!/home/stef/bin/python

import sys
import daltonoutput
import math

dalton = daltonoutput.DaltonOutput(sys.argv[1])

numOfAtoms = dalton.molecule.numOfAtoms

atoms = dalton.molecule.atomList
geometry = dalton.molecule.geometryList[0]


print "       8.     1 ano-1 4 3 1"
print atoms[0].symbol,"         ",geometry.posList[0].x,"            ",geometry.posList[0].y,"          ",geometry.posList[0].z
print "       6.     1 ano-1 4 3 1"
print atoms[1].symbol,"         ",geometry.posList[1].x,"            ",geometry.posList[1].y,"          ",geometry.posList[1].z
print "       1.     1 ano-1 2 1"
print atoms[2].symbol,"         ",geometry.posList[2].x,"            ",geometry.posList[2].y,"          ",geometry.posList[2].z



