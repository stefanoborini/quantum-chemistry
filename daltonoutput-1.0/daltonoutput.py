# Dalton File Parser v1.0 by Stefano Borini 2003

import sys
import string
import re
import math
import filereader
from generalpurpose import ParseError


def normalModeSort(a,b):
	if a.frequency < b.frequency:
		return -1
	elif a.frequency > b.frequency:
		return 1
	else:
		return 0


class Atom:
	def __init__(self):
		self.symbol = ''
		self.charge = 0
		self.mass = 0.0
		self.primitives = 0
		self.contracted = 0
		self.basis = ''
	def __str__(self):
		s = "Atom\n"
		s += "symbol: %s\n" % self.symbol
		s += "charge: %d\n" % self.charge
		s += "mass:   %f\n" % self.mass
		s += "prim:   %d\n" % self.primitives
		s += "contr:  %d\n" % self.contracted
		s += "basis:  %s\n" % self.basis
		return s

class Position:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
	def __str__(self):
		return '(%f,%f,%f)\n' % (self.x,self.y,self.z)

class Geometry:
	def __init__(self):
		self.posList=[]
		self.energy=0.0
	def __str__(self):
		s = 'Geometry\n'
		for i in self.posList:
			s += str(i)
		s += "energy: %f\n" % self.energy
		return s

class Molecule:
	def __init__(self):
		self.numOfAtoms=0
		self.numOfAtomTypes=0
		self.atomList = []
		self.geometryList = []
		self.normalModeList = []
	def __str__(self):
		s = "Molecule\n"
		for i in self.atomList:
			s += str(i)
		for i in self.geometryList:
			s += str(i)
		for i in self.normalModeList:
			s += str(i)
		return s
	def lastGeometry(self):
		return self.geometryList[len(self.geometryList)-1]

class NormalMode:
	def __init__(self):
		self.frequency=0
		self.coordinates=[]
	def __str__(self):
		s = "Normal Coordinate\n"
		s += "frequency:  %f\n" % self.frequency
		s += "coordinates: %s\n" % str(self.coordinates)
		return s

class DaltonOutput:
	def __getAtoms(self):
		"""Build the atom list for the molecule
		"""
		molecule = self.__molecule
		file = self.__fd
		file.toBOF()
		ret = file.findString("Atoms and basis sets")
		if ret == '':
			raise ParseError("Keyword not found 'Atoms and basis sets'")
		file.skipLines(2)
		line = file.readline()
		molecule.numOfAtomTypes=int(re.compile("Number of atom types:\s*([0-9]+)").search(line).group(1))
		line = file.readline()
		molecule.numOfAtoms=int(re.compile("Total number of atoms:\s*([0-9]+)").search(line).group(1))
		#  O           1       8      42      30      [10s5p2d1f|4s3p2d1f]
		file.skipLines(3)
		regexp=re.compile("^\s*(.+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\[.*\])\s+")
		for i in xrange(0,self.__molecule.numOfAtomTypes):
			line = file.readline()
			res = regexp.match(line)
			numForThisAtomType=int(res.group(2))
			for j in xrange(0,numForThisAtomType):
				atom = Atom()
				atom.symbol = res.group(1)
				atom.charge = int(res.group(3))
				atom.primitives = int(res.group(4))
				atom.contracted = int(res.group(5))
				atom.basis = res.group(6)
				molecule.atomList.append(atom)


	def __getGeometry(self):

		# get the starting geometry
		file = self.__fd
		file.toBOF()
		ret = file.findString("Cartesian Coordinates")
		if ret == '':
			raise ParseError("Keyword not found 'Cartesian Coordinates'")
		file.skipLines(5)
		# catches    1   O        x      0.0000000000
		# and also   7   H    1   x      0.0000000000
		regexp1=re.compile("^\s+\d+\s+.+\s+.+\s+x\s+(-?\d+\.\d+)\s*")
		# catches    2            y      0.0000000000
		regexp2=re.compile("^\s+\d+\s+[yz]\s*(-?\d+\.\d+)\s*")
		geometry = Geometry()
		self.__molecule.geometryList.append(geometry)
		for i in xrange(0,self.__molecule.numOfAtoms):
			pos = Position()

			line=file.readline()
			res=regexp1.search(line)
			pos.x=float(res.group(1))

			line=file.readline()
			res=regexp2.search(line)
			pos.y=float(res.group(1))

			line=file.readline()
			res=regexp2.search(line)
			pos.z=float(res.group(1))

			geometry.posList.append(pos)

			file.readline()

		# get the energy
		
		ret=file.findRegexp("^\s*Final\s+.*\senergy:\s*(-\d+\.\d+)\s*$")
		
		if ret[0] == '':
			raise ParseError('No Final energy in this output')

		geometry.energy=float(ret[1][0])
		
		# try to get other geometries from the optimization
		
		save = file.currentPos()
		ret = file.findString("Next geometry (au)")
		if ret == '':
			# there are no other geometries
			return
		file.toPos(save)
		
		geolist = file.occurrences("Next geometry (au)")

		for i in geolist:
			file.toPos(i)
			file.skipLines(2)
			regexp=re.compile("^\s+.*\s+\d*\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$")
			geometry = Geometry()
			self.__molecule.geometryList.append(geometry)
			for j in xrange(0,self.__molecule.numOfAtoms):
				pos = Position()
				line=file.readline()
				res=regexp.search(line)
				pos.x=float(res.group(1))
				pos.y=float(res.group(2))
				pos.z=float(res.group(3))
				geometry.posList.append(pos)
			# catch the subsequent energy
			ret=file.findRegexp("^\s*Final\s+.*\senergy:\s*(-\d+\.\d+)\s*$")
			if ret[0] == '':
				raise ParseError('No Final energy in this output during optimization, pos %d' % i)
	
			geometry.energy=float(ret[1][0])
		
	def __getMasses(self):
		# try to gather the masses... these data could not be present,
		# since isotopic masses are given only when a geometry optimization
		# is requested
		file = self.__fd
		file.toBOF()
		ret = file.findString("Isotopic Masses")
		if ret == '':
			return
		file.skipLines(2)
		regexp=re.compile("^\s*.+\s+\d*\s+(\d+\.\d+)")
		
		for i in xrange(0,self.__molecule.numOfAtoms):
			line=file.readline()
			res=regexp.search(line)
			atom=self.__molecule.atomList[i]
			atom.mass = float(res.group(1))

	def __getVibrational(self):
		""" 
		parse and read the vibrational section for the current molecule.
		Note that the format of this section in dalton 1.2 is

		            Eigenvalues of mass-weighted Hessian
		            ------------------------------------
		
		
		        Column   1     Column   2     Column   3     Column   4
		1     1.279649E-42   1.279649E-42   4.094095E-04   9.790871E-44
		
		        Column   5     Column   6
		1     9.790871E-44  -1.212226E-21
		
		
		           Normal coordinates in Cartesian basis
		           -------------------------------------
		
		
		        Column   1     Column   2     Column   3     Column   4
		1       0.02333068     0.00000000     0.00000000     0.00000000
		2       0.00000000     0.02333068     0.00000000     0.00000000
		3       0.00000000     0.00000000     0.02273544     0.00000000
		4       0.00000000     0.00000000     0.00000000     0.00537355
		6       0.00000000     0.00000000    -0.00120607     0.00000000
		
		        Column   5     Column   6
		3       0.00000000     0.00523645
		5       0.00537355     0.00000000
		6       0.00000000     0.00523645
	
		So note that
		- informations are represented in blocks of 4 columns at a time.
		- rows which have zero values for each column aren't written
		"""

		file = self.__fd
		file.toEOF()
		line = file.findString("Eigenvalues of mass-weighted Hessian",1,1)
		if line == '':
			return
		file.skipLines(4)
		
		degOfFreedom = self.__molecule.numOfAtoms*3
		# in the above example, 2 blocks, one made with 4 columns,
		# the other made of 2 columns
		numOfBlocks = ( degOfFreedom + 3 ) / 4 
		# how many columns make the last block, in the above case 2
		# (the columns 5 and 6)
		lastLineEntries = degOfFreedom % 4
		if lastLineEntries == 0:
			lastLineEntries = 4

		eigenvalues=[]
		for i in xrange(0,numOfBlocks):
			columns = 4
			if i == numOfBlocks - 1 : # is the last block
				columns = lastLineEntries
			restring = "^\s+\d*\s+"
			for j in xrange(0,columns):
				restring=restring + "(-?\d\.\d+[DdEe][+-]\d\d)"
				if j == columns - 1:
					restring=restring+"\s*$"
				else:
					restring=restring+"\s+"
			
			regexp = re.compile(restring)
			line = file.readline()
			res=regexp.search(line)	
			transl=string.maketrans('dD','ee')
			for j in xrange(0,columns):
				eigenvalues.append(float(string.translate(res.group(j+1),transl)))
			file.skipLines(2)
		
  
		# get the normal modes
		
		line = file.findString("Normal coordinates in Cartesian basis")
		if line == '':
			raise ParseError("Unable to find keyword 'Normal coordinates in Cartesian basis'")
		
		file.skipLines(4)
		
		eigenvectors=[]
		for i in xrange(0,numOfBlocks):
			columns = 4
			eig=[]
			if i == numOfBlocks - 1: # is the last block
				columns = lastLineEntries
			restring="^\s+(\d+)\s+"
			for j in xrange(0,columns):
				restring = restring + "(-?\d\.\d+)"
				if j == columns - 1:
					restring = restring + "\s*$"
				else:
					restring = restring + "\s+"

			regexp = re.compile(restring)
			for j in xrange(0,columns):
				eig.append([])
			
			lastExistingEntry=0
			j = 0
			while j < degOfFreedom:
				line = file.readline()
				res=regexp.search(line)
				if res == None:
					# this means that we are at the end but some of the
					# remaining data misses 'cause they are zero
					for k in xrange(lastExistingEntry,degOfFreedom):
						for l in xrange(0,columns):
							eig[l].append(0.0)
					break
				else:
					if int(res.group(1)) != j+1:
						# a number was skipped in the dalton printout,
						# because the printing routine automatically
						# eat lines with all zeroes. We need the zeroes,
						# so we take control over the line-by-line reading
						# routine and place the missing zeroes
						for k in xrange(lastExistingEntry+1,int(res.group(1))):
							for l in xrange(0,columns):
								eig[l].append(0.0)
							j = j + 1
					for l in xrange(0,columns):
						eig[l].append(float(string.translate(res.group(l+2),transl)))
					lastExistingEntry=int(res.group(1))
					j = j + 1

			# finished reading the block... put the eigenvectors
			# in the array
			for l in xrange(0,columns):
				eigenvectors.append(eig[l])
			# and step to the next block
			file.skipLines(2)
			
		
		# pack them into normalMode objects
	
		for i in xrange(0,degOfFreedom):
			normalmode = NormalMode()
			normalmode.frequency=math.sqrt(abs(eigenvalues[i]))
			if eigenvalues[i] < 0:
				normalmode.frequency = - normalmode.frequency
			normalmode.coordinates=eigenvectors[i]
			self.__molecule.normalModeList.append(normalmode)

		# sort the NormalMode list

		self.__molecule.normalModeList.sort(normalModeSort)

	def molecule(self):
		return self.__molecule 
	def filename(self):
		return self.__filename
		
	def __init__(self,filename):
		self.__filename=filename
		self.__fd=filereader.FileReader(self.__filename)
		self.__molecule = Molecule()
		self.__getAtoms()
		self.__getGeometry()
		self.__getMasses()
		self.__getVibrational()


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Usage: %s filename" % sys.argv[0]
		sys.exit()
	m=DaltonOutput(sys.argv[1])
	print m.molecule()




