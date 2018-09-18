import math

class ParseError(Exception):
	def __init__(self, message, filename="Unknown", linenum="Unknown"):
		self.__message = message
		self.__filename = filename
		self.__linenum = linenum
	def __str__(self):
		string = 'Error parsing file \"%s\":%s : %s' % (self.__filename,self.__linenum,self.__message)
		return string

class Vector:
	def __init__(self,coords=None):
		if (coords == None):
			coords =(0.0,0.0,0.0)
		self.__value=list(coords)
	def translate(self,vector):
		self.__value[0]=self.__value[0]+vector[0]
		self.__value[1]=self.__value[1]+vector[1]
		self.__value[2]=self.__value[2]+vector[2]
	def value(self):
		return tuple(self.__value)
	def setValue(self,coords):
		self.__value=list(coords)
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
	def negative(self):
		return (-self.__value[0],-self.__value[1],-self.__value[2])


