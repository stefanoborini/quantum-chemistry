import sys
import csv

from math import sqrt, fabs
def pdis(a, b, c):
    """computes the minimum distance between a line (defined by two 2D points a,b) and a 2D point c"""
    t = b[0]-a[0], b[1]-a[1]           # Vector ab
    dd = sqrt(t[0]**2+t[1]**2)         # Length of ab
    t = t[0]/dd, t[1]/dd               # unit vector of ab
    n = -t[1], t[0]                    # normal unit vector to ab
    ac = c[0]-a[0], c[1]-a[1]          # vector ac
    return ac[0]*n[0]+ac[1]*n[1] # Projection of ac to n (the minimum distance)



if len(sys.argv) < 3:
    print "Usage: "+sys.argv[0]+" regression_info.csv 2d_point_set.csv"
    sys.exit(1)


m = q = r = two_tail = stderr = None

regression_file=file(sys.argv[1],"r")

for row in csv.reader(regression_file):
    if len(row) == 0 or len(row[0].strip()) == 0 or row[0].strip()[0] == "#":
        continue
    if len(row) == 5:
        m, q, r, two_tail, stderr = map(float, row)
        break

regression_file.close()


points_file=file(sys.argv[2],"r")
for row in csv.reader(points_file):
    if len(row) == 0 or len(row[0].strip()) == 0 or row[0].strip()[0] == "#":
        continue
    if len(row) == 2:
        point = tuple(map(float, row))
        print pdis( (0.0,q), (50,50*m+q), point ) 
    
