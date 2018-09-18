import math 
from theochempy._theochempy.ComputerScience import deprecated

class Vector:
    @deprecated("use Vector3 instead")
    def __init__(self,x,y,z):
        self.__value=[x,y,z]
    @deprecated("")
    def translate(self,x,y,z):
        self.__value[0]=self.__value[0]+x
        self.__value[1]=self.__value[1]+y
        self.__value[2]=self.__value[2]+z
    @deprecated("")
    def value(self):
        return self.__value
    @deprecated("")
    def matProd(self,mat):
        tmp=[0,0,0]
        tmp[0]=self.__value[0]*mat[0][0]+self.__value[1]*mat[1][0]+self.__value[2]*mat[2][0]
        tmp[1]=self.__value[0]*mat[0][1]+self.__value[1]*mat[1][1]+self.__value[2]*mat[2][1]
        tmp[2]=self.__value[0]*mat[0][2]+self.__value[1]*mat[1][2]+self.__value[2]*mat[2][2]
        self.__value=tmp
    @deprecated("")
    def rotateX(self,ang):
        mat=[[1,0,0],[0,1,0],[0,0,1]]
        mat[1][1]=math.cos(ang)
        mat[1][2]=-math.sin(ang)
        mat[2][1]=math.sin(ang)
        mat[2][2]=math.cos(ang)
        self.matProd(mat)
    @deprecated("")
    def rotateY(self,ang):
        mat=[[1,0,0],[0,1,0],[0,0,1]]
        mat[0][0]=math.cos(ang)
        mat[0][2]=-math.sin(ang)
        mat[2][0]=math.sin(ang)
        mat[2][2]=math.cos(ang)
        self.matProd(mat)
    @deprecated("")
    def rotateZ(self,ang):
        mat=[[1,0,0],[0,1,0],[0,0,1]]
        mat[0][0]=math.cos(ang)
        mat[0][1]=-math.sin(ang)
        mat[1][0]=math.sin(ang)
        mat[1][1]=math.cos(ang)
        self.matProd(mat)
    @deprecated("")
    def __getitem__(self,idx):
        return self.__value[idx]
    @deprecated("")
    def __setitem__(self,idx,val):
        self.__value[idx]=val
    @deprecated("")
    def x(self):
        return self.__value[0]
    @deprecated("")
    def y(self):
        return self.__value[1]
    @deprecated("")
    def z(self):
        return self.__value[2]

