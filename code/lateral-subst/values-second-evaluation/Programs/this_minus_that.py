import sys
this=file(sys.argv[1])
that=file(sys.argv[2])

this_data=[float(x.strip()) for x in this.readlines()]
that_data=[float(y.strip()) for y in that.readlines()]

if len(this_data) != len(that_data):
    raise Exception("len not equal")

res = []
for a,b in zip(this_data, that_data):
    res.append(str( (a-b)*1000) )

print ",".join(res) 
