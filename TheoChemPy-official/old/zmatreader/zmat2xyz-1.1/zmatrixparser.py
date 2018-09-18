import ptable
import math
from generalpurpose import Vector
from copy import copy, deepcopy

class ParseException(Exception):
	Error_None, Error_Internal, Error_Parse, Error_Unknown = range(4)
	def __init__(self, message="", line=0, code=Error_Unknown):
		self.message = message
		self.line = line
		self.code = code
	def __str__(self):
		return self.message


class ZMatrixParser:
	"""This class parses the zmatrix section, given as a list of lines. It
	stores the results in this format: distances -> always in bohr
	angles & dihedrals -> always in radians
	"""
# Enums
	Format_Internal, Format_Gaussian, Format_Dalton = range(3)
	Unit_DistanceBohr, Unit_DistanceAngstrom = range(2)
	Unit_AngleRadians, Unit_AngleDegrees = range(2)
	Unit_DihedralRadians, Unit_DihedralDegrees = range(2)

	# the positions in the internal format. These offsets are
	# both for the Internal Format representation in the file
	# and in the class internal array itself.
	# AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]
	Internal_AtomListSymbol,Internal_AtomListId,Internal_AtomListBondId=range(3)
	Internal_AtomListBondValue,Internal_AtomListAngleId,Internal_AtomListAngleValue=range(3,6)
	Internal_AtomListDihedralId,Internal_AtomListDihedralValue=range(6,8)



# internal variables
	
	__distanceUnit = Unit_DistanceBohr
	__angleUnit = Unit_AngleDegrees
	__dihedralUnit = Unit_DihedralDegrees
	__format = Format_Internal

# Member classes
	def __init__(self):
		self.__zmatrix=[]

	def parse(self,zmatrix):
		# {{{
		self.__zmatrix=[]
		# clear the current zmatrix
		if self.__format == self.Format_Internal:
			self.__parseInternal(zmatrix)
		elif self.__format == self.Format_Gaussian:
			self.__parseGaussian(zmatrix)
		elif self.__format == self.Format_Dalton:
			self.__parseDalton(zmatrix)
		else:
			raise ParseException("Unknown value for format property",Error_Internal)
		# }}}
		
	def setDistanceUnit(self, value):
		# {{{
		if value in [self.Unit_DistanceBohr, self.Unit_DistanceAngstrom]:
			self.__distanceUnit = value
			return
		else:
			raise ParseException("Unknown value for setDistanceUnit",Error_Internal);
		# }}}

	def getDistanceUnit(self):
		# {{{
		return self.__distanceUnit
		# }}}

	def setAngleUnit(self, value):
		# {{{
		if value in [self.Unit_AngleRadians,self.Unit_AngleDegrees]:
			self.__angleUnit = value
			return
		else:
			raise ParseException("Unknown value for setAngleUnit",Error_Internal);
		# }}}

	def getAngleUnit(self):
		# {{{
		return self.__angleUnit
		# }}}

	def setDihedralUnit(self, value):
		# {{{
		if value in [self.Unit_DihedralRadians,self.Unit_DihedralDegrees]:
			self.__dihedralUnit = value
			return
		else:
			raise ParseException("Unknown value for setDihedralUnit",Error_Internal);
		# }}}

	def getDihedralUnit(self):
		# {{{
		return self.__dihedralUnit
		# }}}

	def setFormat(self,value):
		# {{{
		if value in [self.Format_Internal,self.Format_Gaussian,self.Format_Dalton]:
			self.__format = value
			return
		else:
			raise ParseException("Unknown value for setFormat",Error_Internal);
		# }}}

	def getFormat(self):
		# {{{
		return self.__format
		# }}}


	def cartesianCoords(self):
# {{{
		cart=[]
		zmatrix = self.__zmatrix
		for currentAtom in zmatrix:
			carttmp=[]
			if zmatrix.index(currentAtom) == 0:
				# first atom, place in the center
				# FIXME move to parent
				#if self.__basis.has_key( int(currentAtom[self.AtomListId]) ):
				#		basis = self.__basis[ int(currentAtom[self.AtomListId] ) ]
				#else:
				#	basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.AtomListId]) 
				cart.append( (currentAtom[self.Internal_AtomListSymbol], (0.0,0.0,0.0)))
			elif zmatrix.index(currentAtom) == 1:
				# the second atom. Place along the z axis at the bond distance
				# FIXME move to parent
				#if self.__basis.has_key( int(currentAtom[self.Internal_AtomListId]) ):
				#	basis = self.__basis[ int(currentAtom[self.Internal_AtomListId] ) ]
				#else:
				#	basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.AtomListId]) 
				cart.append( (currentAtom[self.Internal_AtomListSymbol], (0.0, 0.0, currentAtom[self.Internal_AtomListBondValue])))
			elif zmatrix.index(currentAtom) >= 2:
				# {{{
				# third atom and subsequent. copy into a temporary buffer the cart position of 1 and 2
				# WARNING: atom 1 for zmatrix enumeration is element 0 in the cartesian list
				# so always decrease indexes by one.
				idx = currentAtom[self.Internal_AtomListBondId]-1
				carttmp.append( deepcopy(cart[idx]) )
				idx = currentAtom[self.Internal_AtomListAngleId]-1
				carttmp.append( deepcopy(cart[idx]) ) 
				# center the bond reference angle
				# now carttmp holds:
				# in position 0 the bond lenght reference atom
				# in position 1 the angle reference atom

				# if the atom index impose a dihedral existence, load it
				if zmatrix.index(currentAtom) >= 3:
					idx = int(currentAtom[self.Internal_AtomListDihedralId])-1
					carttmp.append( deepcopy(cart[idx]) ) 
					# now carttmp also holds:
					# in position 2 the dihedral reference atom

				TheAtom=carttmp[0]
				TheAtomCoords = TheAtom[1]
				v = Vector()

				# translate each atom by carttmp
				for i in xrange(len(carttmp)):
					atom=list(carttmp[i])
					v.setValue(atom[1])
					v.translate((-TheAtomCoords[0],-TheAtomCoords[1],-TheAtomCoords[2]))
					atom[1] = v.value()
					carttmp[i]=tuple(atom)
				# keep the translated transformation, to revert it later
				translation=TheAtomCoords

				# done... now carttmp holds the translated elements.
				# now work on the second atom, rotate the whole carttmp so to have
				# the second atom on z

				TheAtom=carttmp[1]
				TheAtomCoords = TheAtom[1]

				# the length of zy
				
				ryz=math.sqrt(TheAtomCoords[1]**2+TheAtomCoords[2]**2)
				if ryz > 1e-10:
					# the cosine of the angle
					rapp=TheAtomCoords[2]/ryz
					# choose the correct quadrant
					sign=1
					if TheAtomCoords[1] < 0:
						sign=-1
					xangle=sign*math.acos(rapp)
				else:
					if TheAtomCoords[1] < 0:
						xangle=math.pi
					else:
						xangle=0.0
					
				# now rotate all examined atoms along x
				for i in xrange(len(carttmp)):
					atom=list(carttmp[i])
					v.setValue(atom[1])
					v.rotateX(-xangle)
					atom[1] = v.value()
					carttmp[i]=tuple(atom)

				TheAtom=carttmp[1]
				TheAtomCoords = TheAtom[1]

				# do the same on the y axis
				# the lenght of xz
				rxz=math.sqrt(TheAtomCoords[0]**2+TheAtomCoords[2]**2)

				if rxz > 1e-10 :
					# the cosine of the angle
					rapp=TheAtomCoords[2]/rxz
					# choose the correct quadrant
					sign=1
					if TheAtomCoords[0] < 0:
						sign=-1
					yangle=sign*math.acos(rapp)
				else:
					if TheAtomCoords[0] < 0:
						yangle=math.pi
					else:
						yangle=0.0
	
				# now rotate along y
				for i in xrange(len(carttmp)):
					atom = list(carttmp[i])
					v.setValue(atom[1])
					v.rotateY(-yangle)
					atom[1] = v.value()
					carttmp[i] = tuple(atom)
				
				zangle = 0.0

				if zmatrix.index(currentAtom) >= 3:
					# dihedral
					
					TheAtom=carttmp[2]
					TheAtomCoords = TheAtom[1]
					print TheAtom

					rxy=math.sqrt(TheAtomCoords[0]**2+TheAtomCoords[1]**2)
					if rxy > 1e-10 :
						rapp=TheAtomCoords[1]/rxy
						sign=1
						if TheAtomCoords[0] < 0:
							sign=-1
						zangle=sign*math.acos(rapp)
					else:
						raise ParseException('Third atom %d is collinear with %d and %d at specification for atom %d' % (currentAtom[self.Internal_AtomListDihedralId], currentAtom[self.Internal_AtomListBondId],currentAtom[self.Internal_AtomListAngleId],currentAtom[self.Internal_AtomListId]),0,ParseException.Error_Parse)
		
					for i in xrange(len(carttmp)):
						atom = list(carttmp[i])
						v.setValue(atom[1])
						v.rotateZ(-zangle)
						atom[1] = v.value()
						carttmp[i] = tuple(atom)
					
				# keep the rotation transformation close at hand, to revert it later
				rotation=(xangle, yangle, zangle)
				
				# it's time to place our new atom

				newAtomPos=(0.0, 0.0, float(currentAtom[self.Internal_AtomListBondValue]))
				v.setValue(newAtomPos)
				angle=float(currentAtom[self.Internal_AtomListAngleValue])*math.pi/180
				v.rotateX(angle)

				if zmatrix.index(currentAtom) >= 3:
					angle=float(currentAtom[self.Internal_AtomListDihedralValue])*math.pi/180
					v.rotateZ(angle)
				
				# ok.. time to backtransform and regain the position against the
				# original system. Rotate only the current atom vector, since
				# we no longer care about the other atoms.

				# if no dihedral, this first backrotation is zero
				v.rotateZ(rotation[2])
				v.rotateY(rotation[1])
				v.rotateX(rotation[0])
				v.translate(translation)

				# time to add the atom to our cartesian list
				#if self.__basis.has_key( int(currentAtom[self.Internal_AtomListId]) ):
				#	basis = self.__basis[ int(currentAtom[self.Internal_AtomListId] ) ]
				#else:
				#	basis = ''
				#print '-> basis ',basis,' ', int(currentAtom[self.Internal_AtomListId]) 
				cart.append( (currentAtom[self.Internal_AtomListSymbol], v.value()))
				# }}}

				
		return cart
		# }}}
		

	def __parseInternal(self,zmat):
		# {{{
		"""parse the zmatrix in our internal format"""
		pt=ptable.PTable()
		currentLine=0 
		
		while 1:
			try:
				line = zmat[currentLine]
			# the line does not exists, so it's time to close our business
			except IndexError:
				return


			elems = line.split()
			expectedElems = (currentLine+1)*2
			if expectedElems > 8:
				expectedElems = 8
	# {{{ check if line is valid
			if len(elems) != expectedElems:
				print line
				raise ParseException('Wrong format. Expected num. of elements %d found %d' % (expectedElems, len(elems)), currentLine, ParseException.Error_Parse)
	
			# parse the consistency of the line
			# does the atomtype exists?
			if pt.getElementBySymbol(elems[self.Internal_AtomListSymbol]) == None:
				print line
				raise ParseException('Unknown atom type %s' % elems[self.Internal_AtomListSymbol],currentLine,ParseException.Error_Parse)
			
			# the current identifier must match the currentLine parameter
			try:
				theid=int(elems[self.Internal_AtomListId])
			except ValueError:
				print line
				raise ParseException('Non integer value as id at field 2' ,currentLine,ParseException.Error_Parse)
	
			if theid != currentLine+1:
				print line
				raise ParseException('Error in identifier. Expected %d, found %d.' % (currentLine, theid),currentLine,ParseException.Error_Parse)
	
			# for each identifier  check if its' integer and lower than the
			# current identifier num (but greater than one! :)), and also if
			# the associated data is numeric
			temp=[]
			for i in range(2,expectedElems,2):
				try:
					theid=int(elems[i])
				except ValueError:
					print line
					raise ParseException('Non integer value as id at field %d' % (i+1),currentLine, ParseException.Error_Parse)
				
				# check if there's no duplicated id in this line
				try:
					temp.index(theid)
				except ValueError:
					pass
				else:
					print line
					raise ParseException('Duplicated id at field %d' % (i+1) , currentLine, ParseException.Error_Parse)
				
				temp.append(theid)
				
				try:
					theval=float(elems[i+1])
				except ValueError:
					print line
					raise ParseException('Non numeric value given as parameter at field %d' % (i+2), currentLine, ParseException.Error_Parse)
				
				if theid < 1 or theid >= currentLine+1:
					print line
					raise ParseException('Wrong id parameter at field %d' % (i+1), currentLine, ParseException.Error_Parse)
				
	# }}}	 
		
			tupleToAdd = []
			# ok... the line seems valid.
			# convert the units in the class internal format, if needed
			# lenghts in bohr, angles in radians
	
			tupleToAdd.append(elems[self.Internal_AtomListSymbol])
			tupleToAdd.append(int(elems[self.Internal_AtomListId]))
			if expectedElems > 2:
				tupleToAdd.append(int(elems[self.Internal_AtomListBondId]))
				tupleToAdd.append(self.__convertDistance(float(elems[self.Internal_AtomListBondValue])))
			if expectedElems > 4:
				tupleToAdd.append(int(elems[self.Internal_AtomListAngleId]))
				tupleToAdd.append(self.__convertAngle(float(elems[self.Internal_AtomListAngleValue])))
			if expectedElems > 6:
				tupleToAdd.append(int(elems[self.Internal_AtomListDihedralId]))
				tupleToAdd.append(self.__convertDihedral(float(elems[self.Internal_AtomListDihedralValue])))
			# Pack the tuple and add to an array
			
			self.__zmatrix.append(tuple(tupleToAdd))
			
			# new line and restart
			currentLine = currentLine + 1
		# }}}

	def __convertDistance(self,value):
		# {{{
		"""	Take the distance in the unit as the property distanceunit
			informs, and convert it in the standard internal value, bohr.
		"""
	
		du = self.__distanceUnit
		if du == self.Unit_DistanceAngstrom:
			return float(value)/0.52917721
		elif du == self.Unit_DistanceBohr:
			return float(value)
	
		raise ParseException("convertDistance not reaching point",0,Error_Internal)
		# }}}
	
	def	__convertAngle(self,value):
		# {{{
		"""	Take the angle in the unit as the property angleunit
			informs, and convert it in the standard internal value, radians.
		"""
	
		au = self.__angleUnit
		if au == self.Unit_AngleDegrees:
			return float(value)*math.pi/180.0
		elif au == self.Unit_AngleRadians:
			return float(value)
	
		raise ParseException("convertAngle not reaching point",0,Error_Internal)
		# }}}
	
	def	__convertDihedral(self,value):
		# {{{
		"""	Take the dihedral in the unit as the property dihedralunit
			informs, and convert it in the standard internal value, radians.
		"""
	
		du = self.__dihedralUnit
		if du == self.Unit_DihedralDegrees:
			return float(value)*math.pi/180.0
		elif du == self.Unit_DihedralRadians:
			return float(value)

		raise ParseException("convertDihedral not reaching point",0,Error_Internal)
		# }}} 

	def zmatrix(self):
		return self.__zmatrix



# {{{ Test Suite
if __name__ == '__main__':

	class TestSuite:
		def __init__(self):
			self.__verbose=0
			self.__parser=ZMatrixParser()
			self.test1()
			self.test2()
			#self.test3()


		def test1(self):
			test="O 1\nC 2 1 2.621380\nX 3 2 1.0 1 90.0\nX 4 2 1.0 1 90.0 3 90.0\nH 5 2 2.037790 1 113.3640 4 141.1710"
			test=test.split('\n')
			expectedRes = [ ('O', 1), ('C',2,1,2.621380), ('X', 3, 2, 1.0, 1, 1.5707963), ('X',4,2,1.0,1,1.5707963,3,1.5707963),('H',5, 2, 2.037790, 1, 1.9785751, 4, 2.4638988) ] 
			self.__parser.parse(test)
			res=self.__parser.zmatrix();

			print "1. Testing a simple zmatrix in internal format"
			print "----------------------------------------------"
			if self.__verbose:
				print "Parser class settings: all default"
				print "ZMatrix settings: format Internal"
				print "                  distances in Bohr"
				print "                  angles in degrees"
				print "                  dihedrals in degrees"
				print "Parsed zmatrix:"
				print test.join('\n')
				print "Expected result:"
				for i in expectedRes:
					print i
				print "Obtained result:"
				for i in res:
					print i
				print "----------------------------------------------"
			if self.__compare(expectedRes,res):
				print "Test 1: good"
			else:
				print "Test 1: BAD!!"

		def test2(self):
			test="O 1\nC 2 1 1.3871746\nX 3 2 0.52917721 1 1.5707963\nX 4 2 0.52917721 1 1.5707963 3 1.5707963\nH 5 2 1.078352 1 1.9785751 4 2.4638988"
			test=test.split('\n')
			expectedRes = [ ('O', 1), ('C',2,1,2.6213801), ('X', 3, 2, 1.0, 1, 1.5707963), ('X',4,2,1.0,1,1.5707963,3,1.5707963),('H',5, 2, 2.0377899, 1, 1.9785751, 4, 2.4638988) ] 
			self.__parser.setDistanceUnit(self.__parser.Unit_DistanceAngstrom)
			self.__parser.setAngleUnit(self.__parser.Unit_AngleRadians)
			self.__parser.setDihedralUnit(self.__parser.Unit_DihedralRadians)
			self.__parser.parse(test)
			res=self.__parser.zmatrix();

			print "2. Testing a simple zmatrix in internal format, using other units"
			print "----------------------------------------------"
			if self.__verbose:
				print "Parser class settings: format Internal"
				print "                       distance in angstrom"
				print "                       angles in radians"
				print "                       dihedrals in radians"
				print "ZMatrix settings: format Internal"
				print "                  distances in Bohr"
				print "                  angles in degrees"
				print "                  dihedrals in degrees"
				print "Parsed zmatrix:"
				print test.join('\n')
				print "Expected result:"
				for i in expectedRes:
					print i
				print "Obtained result:"
				for i in res:
					print i
				print "----------------------------------------------"
			if self.__compare(expectedRes,res):
				print "Test 2: good"
			else:
				print "Test 2: BAD!!"


					
		def __compare(self,expectedRes,res):
			retvalue=1
			if len(expectedRes) != len(res):
				return 0
			l=len(expectedRes)
			for i in xrange(l):
				goodline=list(expectedRes[i])
				testline=list(res[i])
				expectedElems = (i+1)*2
				if expectedElems > 8:
					expectedElems = 8;
				goodline.extend([0.0]*(8-expectedElems))
				testline.extend([0.0]*(8-expectedElems))
				
				for j in [1,2,4,6]:
					goodline[j]=str(goodline[j])
					testline[j]=str(testline[j])
				for j in [3,5,7]:
					goodline[j]="%.7f" % goodline[j]
					testline[j]="%.7f" % testline[j]
	
				if goodline != testline:
					print "good ", goodline
					print "test ", testline
					retvalue=0
					
			return retvalue
			

	t=TestSuite()
			
# }}}
