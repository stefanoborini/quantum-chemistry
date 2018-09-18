import sys
import math

filename=sys.argv[1]

f=file(filename, "r")
lines = f.readlines()
for i in xrange(0,len(lines),2):
    x1,y1 = map(float, lines[i].split(','))
    x2,y2 = map(float, lines[i+1].split(','))
    print str((x1+x2)/2.0)+","+str((y1+y2)/2.0)
