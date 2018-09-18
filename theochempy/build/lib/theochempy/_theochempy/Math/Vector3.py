import math 
import numpy
import Quaternion

import _Gohlke_transformations

from theochempy._theochempy.ComputerScience import deprecated

class Vector3:
    def __init__(self,x,y,z):
        self.__value=[x,y,z]
    def translate(self,x,y,z):
        self.__value[0]=self.__value[0]+x
        self.__value[1]=self.__value[1]+y
        self.__value[2]=self.__value[2]+z
    def value(self):
        return self.__value
    @deprecated("")
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

    def rotate(self, angle, axis): # fold>>
        atom_list = []
        q = Quaternion.Quaternion(axis, angle)
        m = numpy.array(q.toRotationMatrix())
        arr = numpy.array([ self.value()[0], self.value()[1], self.value()[2], 1.0 ])
        rotated = numpy.dot(m, arr)
        self.__value[0] = rotated[0]
        self.__value[1] = rotated[1]
        self.__value[2] = rotated[2]

    # <<fold

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

    def norm(self): # fold>>
        return _Gohlke_transformations.norm(self.__value)
    # <<fold
