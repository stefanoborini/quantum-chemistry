import sys

f=file(sys.argv[1])

data=[float(x.strip()) for x in f.readlines()]

print sum(data)/len(data)
