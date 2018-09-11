import math
import daltonoutput
import Numeric

class NormalModes:
	def __readGeometry(self):
		# parse the dalton output file to gather the normal modes
		# and final geometry.
		dalton=self.__dalton
		numOfAtoms = dalton.molecule.numOfAtoms
		geometry = dalton.lastGeometry()
		self.geometryList=[]

		for i in xrange(0,numOfAtoms):
			self.geometryList.append((geometry.posList[i].x, geometry.posList[i].y, geometry.posList[i].z, dalton.molecule.atomList[i].mass*1822.88848))
		# FIXME: center the molecule in the center of mass

	def __readLMatrix(self):
		# parse the normal modes to build the L matrix
		dalton=self.__dalton
		numOfAtoms = dalton.molecule.numOfAtoms
		degOfFreedom = dalton.molecule.numOfAtoms*3
		self.LMatrix = Numeric.zeros((degOfFreedom,degOfFreedom), Numeric.Float)
		self.frequency = Numeric.zeros((degOfFreedom,), Numeric.Float)
		for i in xrange(0,degOfFreedom):
			self.frequency[i]=dalton.molecule.normalModeList[i].frequency*219474.63137
			for j in xrange(0,degOfFreedom):
				self.LMatrix[i,j]=dalton.molecule.normalModeList[i].coordinates[j]*math.sqrt(dalton.molecule.atomList[j/3].mass*1822.88848)

		
	def __init__(self,filename):

		self.__dalton = daltonoutput.DaltonOutput(filename)

		self.__readGeometry()
		self.__readLMatrix()

	def moveNormalCoord(self,vec):
		vec=Numeric.array(vec,Numeric.Float)
		dalton=self.__dalton
		numOfAtoms = dalton.molecule.numOfAtoms
		# a vector that holds the mass three times, for x y z
		mass=[]
		for i in xrange(0,numOfAtoms):
			value = (dalton.molecule.atomList[i].mass*1822.88848)**(-0.5)
			mass.append(value)
			mass.append(value)
			mass.append(value)

		# extended function. Not part of Numeric package. i do it by myself
		#

		#	def diagmatrix(v,typecode='l'):
		#		v = array(v,copy=0)
		# l = len(v)
		# a=zeros((l,l),typecode=typecode)
		# for i in xrange(0,l):
		# a[i,i]=v[i]
		# return a
		#

		massmat=Numeric.diagmatrix(mass, Numeric.Float)
		result = Numeric.matrixmultiply(vec,self.LMatrix)
		result = Numeric.matrixmultiply(result,massmat)
		newgeom=[]
		for i in self.geometryList:
			newgeom.append(i[0])
			newgeom.append(i[1])
			newgeom.append(i[2])
		
		newgeom=Numeric.array(newgeom, Numeric.Float)
		newgeom=newgeom+result
	
		return newgeom


if __name__ == "__main__":
	import sys
	a=NormalModes(sys.argv[1])

	s=sys.stdin.readline()
	qvec=[]
	for i in s.split():
		qvec.append(float(i))

	q=Numeric.array(qvec, Numeric.Float)
	res=a.moveNormalCoord(q)
	print res

		
	
