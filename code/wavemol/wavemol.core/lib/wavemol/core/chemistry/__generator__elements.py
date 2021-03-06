# creates the element list
import re
f=file("IUPAC-TechReport-2007.csv","r")

print """
# This code automatically generated by __generator__elements.py
# changes to this file will not survive.
from wavemol.core import units

class Element:
    def __init__(self,atomic_number,symbol, mass):
        self._atomic_number = atomic_number
        self._symbol = symbol
        self._mass = mass
    def symbol(self):
        \"\"\"Returns the element symbol\"\"\"
        return self._symbol
    def atomicNumber(self):
        \"\"\"Returns the atomic number\"\"\"
        return self._atomic_number
    def mass(self):
        \"\"\"Returns the mass as a wavemol.core.units.UncertainQuantity object\"\"\"
        return self._mass

_elements=[]

"""

for line in f:
    mass = None
    mass_value = None
    mass_precision = None

    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue

    entities = line.strip().split(",")
    if len(entities) != 4:
        raise Exception("Invalid entry line "+line.strip())
    atomic_number,symbol,name,mass = entities

    if len(atomic_number.strip()) == 0 or len(symbol.strip()) == 0:
        raise Exception("Invalid entry line "+line.strip())
    
    if len(mass.strip()) != 0:
        m1 = re.match("(\d+\.\d+)\((\d)\)", mass)
        m2 = re.match("(\d+)\.(\d+)\(\d\)", mass)

        if not (m1 and m2):
            raise Exception("Invalid entry line "+line.strip())
        mass_value = float(m1.group(1)+m1.group(2))
        mass_precision = float(1.0/(10**int(len(m2.group(2))+1)))
        print symbol+" = Element(atomic_number="+str(atomic_number)+",symbol=\""+symbol+"\",mass=units.UncertainQuantity("+str(mass_value)+", units.dalton, "+str(mass_precision)+"))"
    else:
        print symbol+" = Element(atomic_number="+str(atomic_number)+",symbol=\""+symbol+"\",mass=None)"
    
    print "_elements.append("+symbol+")"

    
print """
def all():
    \"\"\"Returns a list of all element objects\"\"\"
    return _elements
"""
