#!/home/stef/bin/python

import sys
import daltonoutput
import math

dalton = daltonoutput.DaltonOutput(sys.argv[1])

numOfAtoms = dalton.molecule.numOfAtoms

geometry = dalton.lastGeometry()


# print a venus style output

print '      EQUILIBRIUM COORDINATES IN THE P.A. SYSTEM AND ATOMIC MASSES'
for i in xrange(0,numOfAtoms):
	print '     % 20.10f% 20.10f% 20.10f% 25.10f' % (geometry.posList[i].x, geometry.posList[i].y, geometry.posList[i].z, dalton.molecule.atomList[i].mass*1822.88848)
print ''
print '          ** NORMAL MODES (MASS WEIGHTED AND NORMALIZED), FREQ. IN CM-1 **'
print
print

degOfFreedom = dalton.molecule.numOfAtoms*3
numOfBlocks = ( degOfFreedom +  7 ) / 8
lastLineEntries = degOfFreedom % 8
if lastLineEntries == 0:
	lastLineEntries = 8
for i in xrange(0,numOfBlocks):
	columns = 8
	if i == numOfBlocks-1:
		# the last block
		columns = lastLineEntries
	line='    '
	for j in xrange(1,columns+1):
		line = line + '          %5d' % (i*8+j) 
	print line
	print
	print
	line = '      '
	for j in xrange (0,columns):
		line = line + '% 15.8E' % (dalton.molecule.normalModeList[i*8+j].frequency*219474.63137)
	print line	
	print
	print
	
	line = ' '
	for j in xrange (0,degOfFreedom):
		line = '%4d  ' % (j+1)
		for k in xrange(0,columns):
			line = line + '% 15.9f' % (dalton.molecule.normalModeList[i*8+k].coordinates[j]*math.sqrt(dalton.molecule.atomList[j/3].mass*1822.88848))
		print line	

	print
	print
