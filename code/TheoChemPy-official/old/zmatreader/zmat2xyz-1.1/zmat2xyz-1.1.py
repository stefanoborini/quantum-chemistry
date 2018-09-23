#!/home/stef/bin/python
import filereader
from generalpurpose import ParseError,Vector
import re
import string
import math
import zmatrixparser

class ZMat2XYZ:
	"""
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
	
	the [parameters] section declares and defines the values for parameters
	that will be used in the zmatrix. if a parameter is undeclared, the zmatrix
	parser section reports an error.

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


	def __init__(self):
		return

	def parseFile(self,filename):
		self.__infile = filereader.FileReader(filename)
		self.__readParameters()
		self.__readZMat();
		self.__readBasis();
		self.__readSymmetry();
	
	def writeDalton(self,filename):
# {{{
		"""
		this routine prints the dalton .mol format for the given molecule
		"""
		from string import join
		import ptable
		pt=ptable.PTable()

		cartcoord = self.__zmatrixparser.cartesianCoords()
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

# }}}		
				
	def __readParameters(self):
		# {{{
		f = self.__infile
		f.toBOF()

		self.__parameters={}

		linetuple=f.findRegexp("^\s*\[\s*parameters.*\]\s*$")
		line=linetuple[0]
		if f.isAtEOF():
			# no parameter section
			return
		parOptions=[] # no options for now
		optionsDict = self.__buildOptionsDict(line,parOptions)

		regexp = re.compile("^\s*([a-zA-Z]\w*)\s*=\s*(.*)\s*$")
		line = f.readline().strip()
		while not (f.isAtEOF() or line[0] == '['):
			if line == '' or line[0] == "#":
				line = f.readline().strip()
				continue
			match = regexp.match(line)
			if match != None:
				key = match.group(1)
				val = match.group(2)
				# parse the value, in case there's some defined var in it
				val = self.__parseParameters(val)
				# evaluate the expression, in any case
				val = str(eval(val))
				# add the result to the dictionary
				self.__parameters[key] = val
			line = f.readline().strip()
		print self.__parameters
		# }}}
		
	def __readZMat(self):
		# {{{
		# the mighty parser object. He knows everything
		self.__zmatrixparser = zmatrixparser.ZMatrixParser()

		f = self.__infile

		f.toBOF()
		linetuple=f.findRegexp("^\s*\[\s*zmatrix.*\]\s*$")
		line=linetuple[0]
		if f.isAtEOF():
			raise ParseError('Unable to find [zmatrix] section',f.name,f.currentPos()+1)
		zmatOptions=("distanceunit", "angleunit", "dihedralunit", "format")
		optionsDict = self.__buildOptionsDict(line,zmatOptions)

		zmatrixbegin = f.currentPos()+1

		# {{{ check the distance unit flag
		if optionsDict.has_key('distanceunit'):
			if optionsDict['distanceunit'] == 'angstrom':
				self.__zmatrixparser.setDistanceUnit(zmatrixparser.ZMatrixParser.Unit_DistanceAngstrom)
			elif optionsDict['distanceunit'] == 'bohr':
				self.__zmatrixparser.setDistanceUnit(zmatrixparser.ZMatrixParser.Unit_DistanceBohr)
			else:
				raise ParseError('Unknown value for key distanceunit in [zmatrix] section',f.name,f.currentPos()+1)
		else:
			self.__zmatrixparser.setDistanceUnit(zmatrixparser.ZMatrixParser.Unit_DistanceBohr)
		# }}}
		# {{{ check the angle unit flag
		if optionsDict.has_key('angleunit'):
			if optionsDict['angleunit'] == 'radians':
				self.__zmatrixparser.setAngleUnit(zmatrixparser.ZMatrixParser.Unit_AngleRadians)
			elif optionsDict['angleunit'] == 'degrees':
				self.__zmatrixparser.setAngleUnit(zmatrixparser.ZMatrixParser.Unit_AngleDegrees)
			else:
				raise ParseError('Unknown value for key angleunit in [zmatrix] section',f.name,f.currentPos()+1)
		else:
			self.__zmatrixparser.setAngleUnit(zmatrixparser.ZMatrixParser.Unit_AngleDegrees)
		# }}}
		# {{{ check the dihedral unit flag
		if optionsDict.has_key('dihedralunit'):
			if optionsDict['dihedralunit'] == 'radians':
				self.__zmatrixparser.setDihedralUnit(zmatrixparser.ZMatrixParser.Unit_DihedralRadians)
			elif optionsDict['dihedralunit'] == 'degrees':
				self.__zmatrixparser.setDihedralUnit(zmatrixparser.ZMatrixParser.Unit_DihedralDegrees)
			else:
				raise ParseError('Unknown value for key dihedralunit in [zmatrix] section',f.name,f.currentPos()+1)
		else:
			self.__zmatrixparser.setDihedralUnit(zmatrixparser.ZMatrixParser.Unit_DihedralDegrees)
		# }}}
		# {{{ check the format flag
		if optionsDict.has_key('format'):
			if optionsDict['format'] == 'internal':
				self.__zmatrixparser.setFormat(zmatrixparser.ZMatrixParser.Format_Internal)
			elif optionsDict['format'] == 'gaussian':
				self.__zmatrixparser.setFormat(zmatrixparser.ZMatrixParser.Format_Gaussian)
			elif optionsDict['format'] == 'dalton':
				self.__zmatrixparser.setFormat(zmatrixparser.ZMatrixParser.Format_Dalton)
			else:
				raise ParseError('Unknown value for key format in [zmatrix] section',f.name,f.currentPos()+1)
		else:
			self.__zmatrixparser.setFormat(zmatrixparser.ZMatrixParser.Format_Internal)
		# }}}

		zmat=[]
		line = f.readline().strip()
		while not (f.isAtEOF() or line[0] == '['):
			if line == '' or line[0] == "#":
				# the line is empty or a comment... skip
				line = f.readline().strip()
				continue

			# call the replacement function. It replaces occurences of 
			# parameters into the zmatrix.

			line = self.__parseParameters(line)

			# append the line in a tuple that will be fed into our parser object
			zmat = zmat + [line]
			line = f.readline().strip()

		try:
			self.__zmatrixparser.parse(zmat)
		except ZMatrixParser.ParseException, e:
			raise ParseError('Error type %d in [zmatrix] section: %s' % (e.code, e.message),f.name,zmatrixbegin+e.line+1)
		# }}}

	def __parseParameters(self,line):
# {{{
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
		return line
# }}}

	def __readBasis(self):
# {{{
		basOptions=[] # no options for now
		self.__basis={}
		f = self.__infile
		f.toBOF()
		linetuple=f.findRegexp("^\s*\[\s*basis.*\]\s*$")
		line=linetuple[0]
		if f.isAtEOF():
			# no basis section ? how weird
			return
		optionsDict = self.__buildOptionsDict(line,basOptions)
		
		regexp1 = re.compile("^\s*(\d*)\s+(.*)\s*$")
		regexp2 = re.compile("^\s*([a-zA-Z]\w*)\s+(.*)\s*$")
		regexp3 = re.compile("^\s*"+re.escape("*")+"\s+(.*)\s*$")
		line = f.readline()
		while not (f.isAtEOF() or line.strip()[0] == '['):
			line=string.strip(line)
			if line == '' or line[0] == "#":
				line = f.readline()
				continue
			match1 = regexp1.match(line)
			match2 = regexp2.match(line)
			match3 = regexp3.match(line)
			if match1 != None: # the assignment to an id
				theid = int(match1.group(1))
				if theid > len(self.__zmatrixparser.zmatrix()) or theid < 1:
					raise ParseError('Wrong id parameter %d' % int(theid), f.name,f.currentPos()+1)
				if not self.__basis.has_key(theid):
					self.__basis[theid]=match1.group(2)
			elif match2 != None:
				theatom = match2.group(1)
				list=[]
				for atom in self.__zmatrixparser:
					if atom[self.AtomListSymbol].lower() == theatom.lower():
						list.append(int(atom[self.AtomListId]))
				for i in list:
					if not self.__basis.has_key(i):
						self.__basis[i]=match2.group(2)
			elif match3 != None:
				#print "matched all"
				for i in xrange(1,len(self.__zmatrixparser.zmatrix())+1):
					if not self.__basis.has_key(i):
						self.__basis[i]=match3.group(1)
			line = f.readline()
		#print self.__basis	
# }}}

	def __readSymmetry(self):
# {{{
		self.__symmetries=[]
		check=['X','Y','Z','XY','XZ','YZ','XYZ']
		f = self.__infile
		f.toBOF()
		linetuple=f.findRegexp("^\s*\[\s*symmetry.*\]\s*$")
		line=linetuple[0]
		if f.isAtEOF():
			# no symmetry section
			return
		symOptions=[] # no options for now
		optionsDict = self.__buildOptionsDict(line,symOptions)

		line=f.readline()
			
		self.__symmetries=line.upper().split()

		for k in self.__symmetries:
			if k not in check:
				raise ParseError('Unknown symmetry key %s' % k, f.name,f.currentPos()+1)
# }}}

	def __readPostProcess(self):
# {{{
		postProcessOptions=[] # no options for now
		self.__postProcessoptions={}
		f = self.__infile
		f.toBOF()
		linetuple=f.findRegexp("^\s*\[\s*options.*\]\s*$")
		line=linetuple[0]
		if f.isAtEOF():
			return
		optionsDict = self.__buildOptionsDict(line,optionsOptions)
		
		withoutOptionsDict=[]
		withOptionsDict={"translate" : 0,"xrotate" : 0,"yrotate" : 0,"zrotate" : 0}

		regexp1 = re.compile("^\s*([a-zA-Z]\w*)\s*$")
		regexp2 = re.compile("^\s*([a-zA-Z]\w*)\s*=\s*(.*)\s*$")
		line = f.readline().strip()
		while not (f.isAtEOF() or line.strip()[0] == '['):
			line=string.strip(line)
			if line == '' or line[0] == "#":
				line = f.readline()
				continue
			match1 = regexp1.match(line)
			match2 = regexp2.match(line)
			if match1 != None: # a single keyword
				thekey = match1.group(1)
				if thekey in withoutOptionsKeys:
					# we will think about it when there are withoutOptionsKeys
			elif match2 != None:
				thekey = match2.group(1)
				thevalue = match2.group(2)
				
			line = f.readline()
		#print self.__basis	
# }}}


	def __buildOptionsDict(self, line , options):
# {{{
		d={}
		line=line.lower()
		for opt in options:
			optreg=re.escape(opt.lower())+"\s*=\s*(.+?)[\s\]]"
			regexp=re.compile(optreg)
			m=regexp.search(line)
			if m != None:
				val=m.group(1)
				d[opt]=val
		return d
# }}}			




def usage():
	print 'Usage: %s [-h] -i inputfile -o outputfile [-f output format]' % sys.argv[0]
	print ''
	print 'Output format can be dalton, molcas, gaussian'
	print ''
	print 'If no input or output file is specified, reading and writing'
	print 'Are done via stdin and stdout, respectively.'


if __name__ == '__main__':
	import os
	import sys
	import getopt

	Format_Dalton, Format_Molcas, Format_Gaussian = range(3)
	infilename = ''
	outfilename = ''
	format = Format_Dalton
	
	options="hi:o:f:"
	longopt=["help","input=","output=","format="]

	try:
		opts,args=getopt.getopt(sys.argv[1:],options,longopt)
	except getopt.GetoptError:
		usage()
		sys.exit()
	
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
			sys.exit()
		if o in ("-o","--output"):
			outfilename = a
		if o in ("-i","--input"):
			infilename = a
		if o in ("-f","--format"):
			if a == "dalton":
				format = Format_Dalton
			elif a == "molcas":
				format = Format_Molcas
			elif a == "gaussian":
				format = Format_Gaussian
			else:
				usage()
				sys.exit()

	if infilename == "":
		usage()
		sys.exit()
	if outfilename == "":
		usage()
		sys.exit()
	if format != Format_Dalton:
		print "Only Dalton format supported!!"
		sys.exit()

	parser=ZMat2XYZ()
	parser.parseFile(infilename)
	parser.writeDalton(outfilename)

