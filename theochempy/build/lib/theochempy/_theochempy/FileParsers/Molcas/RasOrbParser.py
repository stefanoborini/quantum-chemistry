import myfile
import generalpurpose
import re

class ParseError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return `self.value`

class Orbital:
	def __init__(self):
		self.coefficient=[]
		self.occupationNumber=0.0;

class Symmetry:
	def __init__(self):
		self.orbital={}
		self.numOfCoefficients=0
	def debug(self):
		print self.orbital


class RasOrbParser:
	def __init__(self):
		pass
	def read(self,filename):
		self.__file = myfile.myfile(filename)
		self.title = "" 
		self.__keywordre=[]
		self.__numberre=[]
		self.symmetry={}

		self.__keywordre.append(re.compile("^\*\sRASSCF\s(.*)"))
		self.__keywordre.append(re.compile("^\*\sORBITAL\s*(\d+)\s*(\d+)"))
		self.__keywordre.append(re.compile("^\*\sOCCUPATION\sNUMBERS"))

		# XXX the order is important. 4 3 2 1
		#match 4 columns
		self.__numberre.append(re.compile("([\d|-]\.\d{12}E[+-]\d{2})([\d|-]\.\d{12}E[+-]\d{2})([\d|-]\.\d{12}E[+-]\d{2})([\d|-]\.\d{12}E[+-]\d{2})"))
		#match 3 columns
		self.__numberre.append(re.compile("([\d|-]\.\d{12}E[+-]\d{2})([\d|-]\.\d{12}E[+-]\d{2})([\d|-]\.\d{12}E[+-]\d{2})"))
		#match 2 columns
		self.__numberre.append(re.compile("([\d|-]\.\d{12}E[+-]\d{2})([\d|-]\.\d{12}E[+-]\d{2})"))
		#match 1 column
		self.__numberre.append(re.compile("([\d|-]\.\d{12}E[+-]\d{2})"))
		
		line=self.__file.readline()

		while not self.__file.isAtEOF():
			index = -1
			for reg in self.__keywordre:
				m=reg.match(line)
				if m != None:
					index = self.__keywordre.index(reg)
					break
			if index == 0:
				self.__fillTitle(m.group(1))
			elif index == 1:
				self.__fillOrbital(int(m.group(1)),int(m.group(2)))
			elif index == 2:
				self.__fillOccNum()
			else:
				raise ParseError("index == %d" % index)
			line=self.__file.readline()
		del __file

	def __fillTitle(self,title):
		self.title = title
	def __fillOrbital(self,symindex,orbindex):
		print "Parsing symmetry %d orbital %d" % (symindex, orbindex)
		# try to find an existent symmetry holder for these orbitals
		try:
			sym=self.symmetry[symindex]
		except KeyError:
			sym=Symmetry()
			self.symmetry[symindex]=sym
		
		# create the orbital
		orb=Orbital()

		# for check... the first orbital read marks the number of
		# coefficients in the given symmetry. The next orbitals must
		# which claims the same symmetry must have the same number
		# of coefficients
		coeffnum = 0 
		while 1:
			line=self.__file.readline()
			index = -1;
			for reg in self.__numberre:
				m=reg.match(line)
				if m != None:
					index = self.__numberre.index(reg)
					for i in xrange(1,5-index):
						orb.coefficient.append(float(m.group(i)))
						coeffnum=coeffnum+1
					break
			# no one of the regexp matched. So maybe we finished
			# to read the coefficients for this orbital
			if index == -1:
				self.__file.readbackline()
				# assign the orbital at the symmetry
				sym.orbital[orbindex]=orb
				# now... if it's the first orbital assign the number of
				# coeff for it
				if sym.numOfCoefficients == 0:
					sym.numOfCoefficients = coeffnum
				else: # else check if symmetry and obtained coeff match
					if coeffnum != sym.numOfCoefficients:
						raise ParseError("Wrong number of coefficients for symmetry %d orbital %d" % (symindex,orbindex))
				return
		
	def __fillOccNum(self):
		for cursym in xrange(1,len(self.symmetry)+1):
			sym=self.symmetry[cursym]
			orbNum=len(sym.orbital)
			lineNum = (orbNum + 3) / 4
			lastLineEntries = orbNum % 4
			if lastLineEntries == 0:
				lastLineEntries = 4
			orbIndex = 0

			for i in xrange(0,lineNum):
				line=self.__file.readline()
				if i == lineNum - 1:
					index = 4-lastLineEntries
				else:
					index = 0
				
				reg = self.__numberre[index]
				
				m=reg.match(line)

				if m == None:
					raise ParseError("Parse error while reading occupation number")

				for i in xrange(1,5-index):
					orbIndex = orbIndex + 1
					orb = sym.orbital[orbIndex]
					orb.occupationNumber = float(m.group(i))

#	def write(self,filename):	
#		self.__file = file(filename,"w")
#		file.writeline("* RASSCF average (pseudo-natural) orbitals\n")
#		for cursym in xrange(1,len(self.symmetry)+1):
#			sym=self.symmetry[cursym]
#			orbNum=len(sym.orbital)
#			for curorb in xrange(1,orbNum+1):
#				orb = sym.orbital[curorb]
#				numOfCoeff=len(orb.coefficient)
#				lineNum = (numOfCoeff + 3) / 4
#				if lastLineEntries == 0:
#					lastLineEntries = 4
#				for i in xrange(0,lineNum):
#					if i == lineNum - 1:
#						format = 
					
			



if __name__ == "__main__":
	r=RasOrbParser()
	r.read("./formaldeide.RasOrb")

