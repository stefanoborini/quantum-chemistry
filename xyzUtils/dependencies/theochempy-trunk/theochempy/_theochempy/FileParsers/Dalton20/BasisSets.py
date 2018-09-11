import filereader
import re

class DaltonBasisParser:
	def __init__(self):
		pass

	def parse(self,filename):
		
		f = filereader.FileReader(filename)

		match = f.findRegexp2("^[aA] (\d*)$")

		while match != None:
			print match
			self.__parseBasis(f,match[1])
			match = f.findRegexp2("^[aA] (\d*)$")
		
	def __parseBasis(self,f,atomicNum):
		
		line = f.readline()
		while not f.isAtEOF():
			if line[0]=='$' or re.search("^\s*$",line) != None:
				line=f.readline()
				continue
			if re.search("^[aA] (\d*)$",line) != None:
				break
			print line
			line = f.readline()
		

if __name__ == "__main__":

	f='/home/stef/Programmi/dalton20-old/basis/STO-3G'
	parser = DaltonBasisParser()
	parser.parse(f)

	
