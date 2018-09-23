#!/home/stef/bin/python

# ZMat2XYZ 1.0.1 - By Stefano Borini, Ferrara University, Italy - Dec 2003
# read LICENSE for copying rights. Briefly, GPL V2

import filereader
from generalpurpose import ParseError
import re
import ptable
import string
import math
from copy import copy, deepcopy

# we don't want to use numpy
class Vector:
	def __init__(self,x,y,z):
		self.__value=[x,y,z]
	def translate(self,x,y,z):
		self.__value[0]=self.__value[0]+x
		self.__value[1]=self.__value[1]+y
		self.__value[2]=self.__value[2]+z
	def value(self):
		return self.__value
	def matProd(self,mat):
		tmp=[0,0,0]
		tmp[0]=self.__value[0]*mat[0][0]+self.__value[1]*mat[1][0]+self.__value[2]*mat[2][0]
		tmp[1]=self.__value[0]*mat[0][1]+self.__value[1]*mat[1][1]+self.__value[2]*mat[2][1]
		tmp[2]=self.__value[0]*mat[0][2]+self.__value[1]*mat[1][2]+self.__value[2]*mat[2][2]
		self.__value=tmp
	def rotateX(self,ang):
		mat=[[1,0,0],[0,1,0],[0,0,1]]
		mat[1][1]=math.cos(ang)
		mat[1][2]=-math.sin(ang)
		mat[2][1]=math.sin(ang)
		mat[2][2]=math.cos(ang)
		self.matProd(mat)
	def rotateY(self,ang):
		mat=[[1,0,0],[0,1,0],[0,0,1]]
		mat[0][0]=math.cos(ang)
		mat[0][2]=-math.sin(ang)
		mat[2][0]=math.sin(ang)
		mat[2][2]=math.cos(ang)
		self.matProd(mat)
	def rotateZ(self,ang):
		mat=[[1,0,0],[0,1,0],[0,0,1]]
		mat[0][0]=math.cos(ang)
		mat[0][1]=-math.sin(ang)
		mat[1][0]=math.sin(ang)
		mat[1][1]=math.cos(ang)
		self.matProd(mat)
	def __getitem__(self,idx):
		return self.__value[idx]
	def __setitem__(self,idx,val):
		self.__value[idx]=val
	def x(self):
		return self.__value[0]
	def y(self):
		return self.__value[1]
	def z(self):
		return self.__value[2]
	
	
	


class ZMat2XYZ:
	"""
	ZMat2XYZ 1.0.1 - By Stefano Borini, Ferrara University, Italy - Dec 2003

	initialize the class.
	The requested format for the zmatrix is
	
	[parameters]
	key=value
	[zmatrix]
	AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]
	[basis]
	identifier basis-string
	AtomSymbol basis-string
	* basis-string
	[symmetry]
	symmetry elements
	
	the [parameters] section is optional. It defines the values for parameters
	that will be used in the zmatrix. if a parameter is undeclared, the zmatrix
	parser section reports an error. You can also specify equations.

	the [zmatrix] section is mandatory, and holds the zmatrix with this format

		AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]

	You can use X as an atomsymbol for the dummy atom. It will be removed from
	the final output.

	the [basis] section is optional, and declares the basis set to use for each
	atom. per default, the numerical identifier is needed. If the AtomSymbol 
	is given, the basis set is assigned to all the atoms with that atomic
	symbol. If the special key * is given, the basis set is assigned to all te
	atoms. Be warned that there's a priority, higher at the top line. If you assign
	the basis A to the identifier 1, the subsequent "*" keyword assigns the basis
	B to all the atoms except the one with identifier 1, which preserves the
	already assigned basis.

	[symmetry] section specifies the symmetry elements expected in the molecule.
	The input requests a single line with space separated keys, where keys are 
	x,y,z for yz,xz and xy reflection planes respectively, xy xz yz for the 
	rotation axis with respect to the z,y,x axis and xyz denotes the inversion.
	"""

	AtomListSymbol=0
	AtomListId=1
	AtomListBondId=2
	AtomListBondValue=3
	AtomListAngleId=4
	AtomListAngleValue=5
	AtomListDihedralId=6
	AtomListDihedralValue=7

	def __init__(self):
		return

	def parseFile(self,infile):
		self.__infile = filereader.FileReader(infile)
		self.__readParameters()
		self.__readZMat();
		self.__readBasis();
		self.__readSymmetry();
	
	def __readParameters(self):
		self.__parameters={}
		f = self.__infile
		f.toBOF()
		f.findString("[parameters")
		if f.isAtEOF():
			# no parameter section
			return
		# this re search for key = anything
		regexp = re.compile("^\s*([a-zA-Z]\w*)\s*=\s*(.*)\s*$")
		line = f.readline()
		while not (f.isAtEOF() or line[0] == '['):
			line=string.strip(line)
			if line == '' or line[0] == "#":
				line = f.readline()
				continue
			match = regexp.match(line)
			if match != None:
				val = match.group(2)
				val = self.__parseParameters(val)
				val = str(eval(val))
				self.__parameters[match.group(1)] = val
			line = f.readline()
		
#		#print self.__parameters
		
	def __readZMat(self):
		pt=ptable.PTable()
		self.__zmatrix=[]
		f = self.__infile
		currentRead=0

		f.toBOF()
		f.findString("[zmatrix")
		if f.isAtEOF():
			raise ParseError('Unable to find [zmatrix] section',f.name,f.currentPos()+1)

		line = f.readline()
		# AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]
		while not (f.isAtEOF() or line[0] == '['):
			line=string.strip(line)
			if line == '' or line[0] == "#":
				# the line is empty or a comment... skip
				line = f.readline()
				continue
			currentRead=currentRead+1

			# call the replacement function. It replaces occurences of parameters into the
			# zmatrix. btw.. what about this sub into the parameters list itself?

			line = self.__parseParameters(line)

			elems=line.split()
			expectedElems=currentRead*2
			if expectedElems > 8:
				expectedElems = 8

			if len(elems) != expectedElems:
					print line
					raise ParseError('Wrong format. Expected elements %d found %d' % (expectedElems, len(elems)),f.name,f.currentPos()+1)

			# parse the consistency of the line
			# does the atomtype exists?
			if pt.getElementBySymbol(elems[self.AtomListSymbol]) == None:
				raise ParseError('Unknown atom type %s' % elems[self.AtomListSymbol],f.name,f.currentPos()+1)
			
			# the current identifier must match the currentRead parameter
			try:
				theid=int(elems[self.AtomListId])
			except ValueError:
				raise ParseError('Non integer value as id at field 2' ,f.name,f.currentPos()+1)

			if int(elems[self.AtomListId]) != currentRead:
				raise ParseError('Error in identifier. Expected %d, found %d.' % (currentRead, int(elems[self.AtomListId])),f.name,f.currentPos()+1)

			# for each identifier  check if its' integer and lower than the
			# current identifier num (but greater than one! :)), and also if
			# the associated data is numeric
			temp=[]
			for i in range(2,expectedElems,2):
				try:
					theid=int(elems[i])
				except ValueError:
					raise ParseError('Non integer value as id at field %d' % (i+1) ,f.name,f.currentPos()+1)
				
				# check if there's no duplicated id in this line
				try:
					temp.index(theid)
				except ValueError:
					pass
				else:
					raise ParseError('Duplicated id at field %d' % (i+1) ,f.name,f.currentPos()+1)
				
				temp.append(theid)
				
				try:
					theval=float(elems[i+1])
				except ValueError:
					raise ParseError('Non numeric value given as parameter at field %d' % (i+2), f.name,f.currentPos()+1)
				
				if theid < 1 or theid >= currentRead:
					raise ParseError('Wrong id parameter at field %d' % (i+1), f.name,f.currentPos()+1)
				
			
			
			# ok... the line seems valid.
			# Pack the line in a tuple and add to an array
			
			self.__zmatrix.append(tuple(elems))
			#print tuple(elems)
			
			# new line and restart
			line = f.readline()
		


	def __parseParameters(self,line):
		notseparators=re.compile('[A-Za-z0-9_]')
#		print "line in -> ",line
		for k,v in self.__parameters.items():
			# find the key in our line
			pos=line.find(k)
			if pos >= 0:
				if pos == 0:
					leftsep=''
				else:
					leftsep=line[pos-1]
				if pos + len(k) == len(line):
					rightsep = ''
				else:
					rightsep = line[pos+len(k)]
				m=notseparators.match(leftsep)
				if m != None:
					continue
				m=notseparators.match(rightsep)
				if m != None:
					continue
				# ok... left and right separators are real separators
				# substitute
				line=line[0:pos]+v+line[pos+len(k):]
		#print "line out -> ",line
		return line

	
	def __parseParameters_old(self,line):
		notseparators=re.compile('[A-Za-z0-9_]')
		for k,v in self.__parameters.items():
			# do a fast match, to check if there's some possibility
			# about the presence of the key in the line
			if line.find(k) > 0:
				k = re.escape(k)
				# between spaces
				reg = re.compile("\s"+k+"\s")
				line = reg.sub(" "+v+" ",line)
				# between space and end of line
				reg = re.compile("\s"+k+"$")
				line = reg.sub(" "+v,line)
				# between begin of line and space
				reg = re.compile("^"+k+"\s")
				line = reg.sub(v+" ",line)
				# between begin of line and end of line. I'm not sure this is the best way
				# to do this, but who cares?
				reg = re.compile("^"+k+"$")
				line = reg.sub(v,line)
		
		return line	
		
	def __readBasis(self):
		self.__basis={}
		f = self.__infile
		f.toBOF()
		f.findString("[basis")
		if f.isAtEOF():
			# no basis section
			return
		
		regexp1 = re.compile("^\s*(\d*)\s+(.*)\s*$")
		regexp2 = re.compile("^\s*([a-zA-Z]\w*)\s+(.*)\s*$")
		regexp3 = re.compile("^\s*"+re.escape("*")+"\s+(.*)\s*$")
		line = f.readline()
		while not (f.isAtEOF() or line[0] == '['):
			line=string.strip(line)
			if line == '' or line[0] == "#":
				line = f.readline()
				continue
			match1 = regexp1.match(line)
			match2 = regexp2.match(line)
			match3 = regexp3.match(line)
			if match1 != None: # the assignment to an id
				theid = int(match1.group(1))
				if theid > len(self.__zmatrix) or theid < 1:
					raise ParseError('Wrong id parameter %d' % int(theid), f.name,f.currentPos()+1)
				if not self.__basis.has_key(theid):
					self.__basis[theid]=match1.group(2)
			elif match2 != None:
				theatom = match2.group(1)
				list=[]
				for atom in self.__zmatrix:
					if atom[self.AtomListSymbol].lower() == theatom.lower():
						list.append(int(atom[self.AtomListId]))
				for i in list:
					if not self.__basis.has_key(i):
						self.__basis[i]=match2.group(2)
			elif match3 != None:
				#print "matched all"
				for i in xrange(1,len(self.__zmatrix)+1):
					if not self.__basis.has_key(i):
						self.__basis[i]=match3.group(1)
			line = f.readline()
		#print self.__basis	
	def __readSymmetry(self):
		self.__symmetries=[]
		check=['X','Y','Z','XY','XZ','YZ','XYZ']
		f = self.__infile
		f.toBOF()
		f.findString("[symmetry")
		if f.isAtEOF():
			# no symmetry section
			return

		line=f.readline()
			
		while not (f.isAtEOF() or line[0] == '['):
			line=string.strip(line)
			if line == '' or line[0] == "#":
				line = f.readline()
				continue
			self.__symmetries=line.upper().split()

			for k in self.__symmetries:
				if k not in check:
					raise ParseError('Unknown symmetry key %s' % k, f.name,f.currentPos()+1)
			line=f.readline()


	def writeDalton(self,filename):
		"""
		this routine prints the dalton .mol format for the given molecule
		"""
		from string import join
		pt=ptable.PTable()

		cartcoord = self.__cartesianCoords()

		groups={}

		for i in cartcoord:
			symbol = i[0]
			if symbol == 'X':
				# skip dummy atom printing
				continue
			basis = i[2]
			key = symbol+":"+basis
			if not groups.has_key(key):
				groups[key]=[]
			groups[key].append(i)

		# ok... now produce the .mol input...
		f=file(filename,"w")

		f.write("ATOMBASIS\n")
		f.write("\n")
		f.write("\n")
		s=join(self.__symmetries).upper()
		f.write(" %4d   %2d  %s\n" % (len(groups), len(self.__symmetries), s))
		
		for k,v in groups.items():
			atomsymbol, basis = k.split(':')
			element = pt.getElementBySymbol(atomsymbol)
			f.write( "     %3d. %5d %s\n" % (element.atomicNumber, len(v), basis))
			currentatom = 0
			for coord in v:
				currentatom = currentatom + 1
				f.write( '%.4s%20.15f%20.15f%20.15f\n' % (coord[0]+str(currentatom),coord[1].x(),coord[1].y(),coord[1].z()))
			
				

	def __cartesianCoords(self):
		cart=[]
		
		for currentAtom in self.__zmatrix:
			carttmp=[]
			if self.__zmatrix.index(currentAtom) == 0:
				# first atom, place in the center
				if self.__basis.has_key( int(currentAtom[self.AtomListId]) ):
					basis = self.__basis[ int(currentAtom[self.AtomListId] ) ]
				else:
					basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.AtomListId]) 
				cart.append( (currentAtom[self.AtomListSymbol], Vector(0.0,0.0,0.0),  basis))
			elif self.__zmatrix.index(currentAtom) == 1:
				# the second atom. Place along the z axis at the bond distance
				if self.__basis.has_key( int(currentAtom[self.AtomListId]) ):
					basis = self.__basis[ int(currentAtom[self.AtomListId] ) ]
				else:
					basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.AtomListId]) 
				cart.append( (currentAtom[self.AtomListSymbol], Vector(0.0, 0.0, float(currentAtom[self.AtomListBondValue])), basis))
			elif self.__zmatrix.index(currentAtom) == 2:
				# {{{
				# third atom. copy into a temporary buffer the cart position of 1 and 2
				# WARNING: atom 1 for zmatrix enumeration is element 0 in the cartesian list
				# so always decrease indexes by one. Also remember that zmatrix storagement is
				# per-string. Id's are strings, distances and angles too... always convert to
				# int or float to manage
				idx = int(currentAtom[self.AtomListBondId])-1
				carttmp.append( deepcopy(cart[idx]) )
				idx = int(currentAtom[self.AtomListAngleId])-1
				carttmp.append( deepcopy(cart[idx]) ) 
				# center the bond reference angle
				# now carttmp holds:
				# in position 0 the bond lenght reference atom
				# in position 1 the angle reference atom

				# choose the first atom and set as the center of the world
				# create a new tuple object with the cartesian parameters

				firstAtom=carttmp[0]
				firstAtomCoords=firstAtom[1]
				secondAtom=carttmp[1]
				secondAtomCoords=secondAtom[1]
				newcenter = (firstAtomCoords.x(), firstAtomCoords.y(), firstAtomCoords.z())
				# remember: newcenter is a tuple for xyz

				# translate each atom by carttmp
				for atom in carttmp:
					atom[1].translate(-newcenter[0],-newcenter[1],-newcenter[2])

				# keep the translated transformation, to revert it later

				translation=(newcenter[0],newcenter[1],newcenter[2])

				# done... now carttmp holds the translated elements.
				# please note that firstAtom and secondAtom are a reference in the
				# list carttmp, so they get updated too.
				# now work on the second atom, rotate the whole carttmp so to have
				# the second atom on z

				# the length of zy
				ryz=math.sqrt(secondAtomCoords.y()**2+secondAtomCoords.z()**2)
				if ryz > 1e-10:
					# the cosine of the angle
					rapp=secondAtomCoords.z()/ryz
					# choose the correct quadrant
					sign=1
					if secondAtomCoords.y() < 0:
						sign=-1
					xangle=sign*math.acos(rapp)
				else:
					if secondAtomCoords.y() < 0:
						xangle=math.pi
					else:
						xangle=0.0
					
				# now rotate along x
				for atom in carttmp[:]:
					atom[1].rotateX(-xangle)

				# do the same on the y axis
				# the lenght of xz
				rxz=math.sqrt(secondAtomCoords.x()**2+secondAtomCoords.z()**2)

				if rxz > 1e-10 :
					# the cosine of the angle
					rapp=secondAtomCoords.z()/rxz
					# choose the correct quadrant
					sign=1
					if secondAtomCoords.x() < 0:
						sign=-1
					yangle=sign*math.acos(rapp)
				else:
					if secondAtomCoords.x() < 0:
						yangle=math.pi
					else:
						yangle=0.0
	
				# now rotate along y
				for atom in carttmp:
					atom[1].rotateY(-yangle)
				
				# keep the rotation transformation close at hand, to revert it later
				rotation=(xangle, yangle, 0.0)
				
				# it's time to place our new atom

				vec=Vector(0.0, 0.0, float(currentAtom[self.AtomListBondValue]))
				angle=float(currentAtom[self.AtomListAngleValue])*math.pi/180
				vec.rotateX(angle)
				
				# ok.. time to backtransform and regain the position against the
				# original system. Rotate only the current atom vector, since
				# we no longer care about the other atoms.

				vec.rotateY(rotation[1])
				vec.rotateX(rotation[0])
				vec.translate(translation[0],translation[1],translation[2])

				# time to add the atom to our cartesian list
				if self.__basis.has_key( int(currentAtom[self.AtomListId]) ):
					basis = self.__basis[ int(currentAtom[self.AtomListId] ) ]
				else:
					basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.AtomListId]) 
				cart.append( (currentAtom[self.AtomListSymbol], vec, basis))
				# }}}
			elif self.__zmatrix.index(currentAtom) >= 3:
				# {{{
				# ok... the same as for index = 2, plus the dihedral rotation
				# cut and paste of the previous section, stripped of the comments
				# should we merge with the previous case ?
				idx = int(currentAtom[self.AtomListBondId])-1
				carttmp.append( deepcopy(cart[idx]) )
				idx = int(currentAtom[self.AtomListAngleId])-1
				carttmp.append( deepcopy(cart[idx]) ) 

				# add the dihedral reference angle
				idx = int(currentAtom[self.AtomListDihedralId])-1
				carttmp.append( deepcopy(cart[idx]) ) 

				# now carttmp holds:
				# in position 2 the dihedral reference atom

				firstAtom=carttmp[0]
				firstAtomCoords=firstAtom[1]
				secondAtom=carttmp[1]
				secondAtomCoords=secondAtom[1]
				thirdAtom=carttmp[2]
				thirdAtomCoords=thirdAtom[1]
				newcenter = (firstAtomCoords.x(), firstAtomCoords.y(), firstAtomCoords.z())

				for atom in carttmp:
					atom[1].translate(-newcenter[0],-newcenter[1],-newcenter[2])

				translation=(newcenter[0],newcenter[1],newcenter[2])

				ryz=math.sqrt(secondAtomCoords.y()**2+secondAtomCoords.z()**2)
				if ryz > 1e-10:
					rapp=secondAtomCoords.z()/ryz
					sign=1
					if secondAtomCoords.y() < 0:
						sign=-1
					xangle=sign*math.acos(rapp)
				else:
					if secondAtomCoords.y() < 0:
						xangle=math.pi
					else:
						xangle=0.0
					
				for atom in carttmp:
					atom[1].rotateX(-xangle)

				rxz=math.sqrt(secondAtomCoords.x()**2+secondAtomCoords.z()**2)

				if rxz > 1e-10 :
					rapp=secondAtomCoords.z()/rxz
					sign=1
					if secondAtomCoords.x() < 0:
						sign=-1
					yangle=sign*math.acos(rapp)
				else:
					if secondAtomCoords.x() < 0:
						yangle=math.pi
					else:
						yangle=0.0
	
				for atom in carttmp:
					atom[1].rotateY(-yangle)
				# now we need to rotate the atoms along the z axis so the third
				# atom is on the yz plane

				rxy=math.sqrt(thirdAtomCoords.x()**2+thirdAtomCoords.y()**2)
				if rxy > 1e-10 :
					rapp=thirdAtomCoords.y()/rxy
					sign=1
					if thirdAtomCoords.x() < 0:
						sign=-1
					zangle=sign*math.acos(rapp)
				else:
					raise ParseError('Third atom %d is collinear with %d and %d at specification for atom %d' % (int(currentAtom[self.AtomListDihedralId]), int(currentAtom[self.AtomListBondId]), int(currentAtom[self.AtomListAngleId]), int(currentAtom[self.AtomListId])) ,None,None)
	
				for atom in carttmp:
					atom[1].rotateZ(-zangle)
				
				rotation=(xangle, yangle, zangle)

				# it's time to place our new atom

				vec=Vector(0.0, 0.0, float(currentAtom[self.AtomListBondValue]))
				angle=float(currentAtom[self.AtomListAngleValue])*math.pi/180
				vec.rotateX(angle)
				angle=float(currentAtom[self.AtomListDihedralValue])*math.pi/180
				vec.rotateZ(angle)

				vec.rotateZ(rotation[2])
				vec.rotateY(rotation[1])
				vec.rotateX(rotation[0])
				vec.translate(translation[0],translation[1],translation[2])
				if self.__basis.has_key( int(currentAtom[self.AtomListId]) ):
					basis = self.__basis[ int(currentAtom[self.AtomListId] ) ]
				else:
					basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.AtomListId]) 

				cart.append( (currentAtom[self.AtomListSymbol], vec, basis))

		# }}}
				
		return cart


if __name__ == '__main__':
	import os
	import sys

	if len(sys.argv) < 3:
		print 'Usage: %s inputfile outputfile' % sys.argv[0]
		sys.exit()
	a=ZMat2XYZ()
	a.parseFile(sys.argv[1])
	a.writeDalton(sys.argv[2])


