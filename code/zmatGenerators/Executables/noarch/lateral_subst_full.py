#!/usr/bin/env python
# @author: Stefano Borini

import sys

try:
    number_of_double_bonds=int(sys.argv[1])
    if number_of_double_bonds < 2:
        raise Exception()
except:
    print "Usage : "+sys.argv[0]+" repetitions"
    print """
Script that generates laterally substituted polyacetylenes in a format suitable for the script zmat2input. 
The number of repetition is the amount of repetitions of the central double bond.
lateral substituents are NH2 and NO2 (or H). they are never put too near geometrically (meaning that
two carbons on the same side of the chain are not substituted at the same time)
"""
    sys.exit(1)

SUBST_HYDROGEN = 0
SUBST_NH2 = 1
SUBST_NO2 = 2




def substitutions(size):
    new_vector = []
    if size == 0:
        new_vector.append( ())
    else:
        vector = substitutions(size-1)
        for elem in vector:
            new_vector.append( elem + (SUBST_HYDROGEN,))
            new_vector.append( elem + (SUBST_NH2,))
            new_vector.append( elem + (SUBST_NO2,))

    return new_vector

def noNearStuff(substitution):
    # on one side of the chain
    for pos in xrange(0,len(substitution),2):
        try: 
            substitution[pos+2]
        except:
            break
        if substitution[pos] != SUBST_HYDROGEN and substitution[pos+2] != SUBST_HYDROGEN:
            return False

    # on the other side
    for pos in xrange(1,len(substitution),2):
        try: 
            substitution[pos+2]
        except:
            break
        if substitution[pos] != SUBST_HYDROGEN and substitution[pos+2] != SUBST_HYDROGEN:
            return False

    return True


def toNamedEntry(entry):
    if entry == SUBST_HYDROGEN:
        return "H"
    elif entry == SUBST_NH2:
        return "NH2"
    elif entry == SUBST_NO2:
        return "NO2"
    else:
        return "XX"

def createBackbone(number_of_double_bonds):
    return """
[parameters]
rc1=1.443
rc2=1.355
rch=1.095
rcn=1.136
roh=0.95
rco=1.43
rcn2=1.475
rno=1.214
rnh=1.01
[zmatrix distance_unit="Angstrom" angle_unit="degrees"]
X 1
X 2 1 rch
C 3 2 rch 1 90.0
C 4 3 rc2 2 120.0 1 90.0"""
    number_of_central_units = number_of_double_bonds-2
    for i in xrange (0,number_of_central_units):
        print "C "+str(5+i*2)+" "+str(4+i*2)+" rc1 "+str(3+i*2)+" 120. "+str(2+i*2)+" 180.0"
        print "C "+str(6+i*2)+" "+str(5+i*2)+" rc2 "+str(4+i*2)+" 120. "+str(3+i*2)+" 180.0"

    print "C "+str(5+number_of_central_units*2)+" "+str(4+number_of_central_units*2)+" rc1 "+str(3+number_of_central_units*2)+" 120. "+str(2+number_of_central_units*2)+" 180.0"
    print "C "+str(6+number_of_central_units*2)+" "+str(5+number_of_central_units*2)+" rc2 "+str(4+number_of_central_units*2)+" 120. "+str(3+number_of_central_units*2)+" 180.0"




atom_ids_to_substitute = range(4,number_of_double_bonds*2+2)

for subst in filter( noNearStuff, substitutions(len(atom_ids_to_substitute))):
    filename = "lateral-"+str(number_of_double_bonds)
    s=createBackbone(number_of_double_bonds)
    current_id = 3+number_of_double_bonds*2
    for count,entry in enumerate(subst):
        filename += "_"+str(count)+"-"+toNamedEntry(entry)
        if entry == SUBST_HYDROGEN:
            s += "H "+str(current_id)+" "+str(atom_ids_to_substitute[count])+" rch "+str(atom_ids_to_substitute[count]-1)+" 120.0 "+str(atom_ids_to_substitute[count]-2)+" 0.0"
            current_id += 1
        elif entry == SUBST_NH2:
            s += "N "+str(current_id)+" "+str(atom_ids_to_substitute[count])+" rch "+str(atom_ids_to_substitute[count]-1)+" 120.0 "+str(atom_ids_to_substitute[count]-2)+" 0.0"
            current_id += 1
            s += "H "+str(current_id)+" "+str(current_id-1)+" rnh "+str(atom_ids_to_substitute[count])+" 120.0 "+str(atom_ids_to_substitute[count]-1)+" 180.0" 
            current_id += 1
            s += "H "+str(current_id)+" "+str(current_id-2)+" rnh "+str(atom_ids_to_substitute[count])+" 120.0 "+str(atom_ids_to_substitute[count]-1)+" 0.0" 
            current_id += 1
        elif entry == SUBST_NO2:
            s += "N "+str(current_id)+" "+str(atom_ids_to_substitute[count])+" rch "+str(atom_ids_to_substitute[count]-1)+" 120.0 "+str(atom_ids_to_substitute[count]-2)+" 0.0"
            current_id += 1
            s += "O "+str(current_id)+" "+str(current_id-1)+" rno "+str(atom_ids_to_substitute[count])+" 120.0 "+str(atom_ids_to_substitute[count]-1)+" 180.0" 
            current_id += 1
            s += "O "+str(current_id)+" "+str(current_id-2)+" rno "+str(atom_ids_to_substitute[count])+" 120.0 "+str(atom_ids_to_substitute[count]-1)+" 0.0" 
            current_id += 1
    s += "H "+str(current_id)+" 3 rch 4 120.0 5 0.0"
    current_id += 1
    s += "H "+str(current_id)+" 3 rch 4 120.0 5 180.0"
    current_id += 1
    s += "H "+str(current_id)+" "+str(number_of_double_bonds*2+2)+" rch "+str(number_of_double_bonds*2+1)+" 120.0 "+str(number_of_double_bonds*2)+" 180.0"
    current_id += 1
    s += "H "+str(current_id)+" "+str(number_of_double_bonds*2+2)+" rch "+str(number_of_double_bonds*2+1)+" 120.0 "+str(number_of_double_bonds*2)+" 0.0"
    current_id += 1
    s += """[basis]
* 6-31G*
"""
    print "writing "+filename
    f=file(filename+".zmat","w")
    f.write(s)
    f.close()

