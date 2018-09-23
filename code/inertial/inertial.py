#!/home/stef/bin/python
# this program calculates the main inertial axes, barycentrum and so on
# input format: 
# mass x y z
# for each atom
import sys
import Numeric
import LinearAlgebra

f=file(sys.argv[1])

lines=f.readlines()

atomlist=[]
atom=0
xbar=0
ybar=0
zbar=0
totalmass=0

for i in lines:
	parse=i.split()
	if len(parse) == 0:
		continue
	mass=float(parse[0])
	x=float(parse[1])
	y=float(parse[2])
	z=float(parse[3])
	xbar=xbar+x*mass
	ybar=ybar+y*mass
	zbar=zbar+z*mass
	totalmass=totalmass + mass
	
	atomlist.append((mass,x,y,z))
	

bar=(xbar/totalmass,ybar/totalmass,zbar/totalmass)

# center the molecular system so the barycentrum is zero

recentered=[]

for i in atomlist:
	tmp=list(i)
	tmp[1]=tmp[1]-bar[0]
	tmp[2]=tmp[2]-bar[1]
	tmp[3]=tmp[3]-bar[2]
	
	recentered.append(tmp)

print recentered

xbar=0
ybar=0
zbar=0
mass=0
totalmass=0
# Check: control if now the barycentrum is at 0.0 0.0 0.0 
#for i in recentered:
	#mass=float(i[0])
	#x=float(i[1])
	#y=float(i[2])
	#z=float(i[3])
	#xbar=xbar+x*mass
	#ybar=ybar+y*mass
	#zbar=zbar+z*mass
	#totalmass = totalmass + mass
#
#print xbar/totalmass,ybar/totalmass,zbar/totalmass

# rotational matrix

matrix=Numeric.zeros((3,3),Numeric.Float)

for i in recentered:
	mass,x,y,z = i
	x=0.529177208*x
	y=0.529177208*y
	z=0.529177208*z

	matrix[0,0] += mass * (y**2 + z**2)
	matrix[0,1] -= mass * x * y
	matrix[0,2] -= mass * x * z
	matrix[1,1] += mass * (x**2 + z**2)
	matrix[1,2] -=mass * y * z
	matrix[2,2] += mass * (x**2 + y**2)

matrix[1,0] = matrix[0,1]
matrix[2,0] = matrix[0,2]
matrix[2,1] = matrix[1,2]

print matrix

val,vec = LinearAlgebra.eigenvectors(matrix)

print "val = ",val
print "vec = ",vec


