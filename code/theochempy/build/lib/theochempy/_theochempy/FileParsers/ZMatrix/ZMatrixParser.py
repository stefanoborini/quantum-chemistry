from theochempy._theochempy.IO import FileReader 
from theochempy._theochempy.Chemistry import PeriodicTable
from theochempy._theochempy import Math
from theochempy._theochempy import Units

import copy
import re
import string
import math
import StringIO

class ParseError(Exception):
    def __init__(self, message, filename="Unknown", linenum="Unknown"):
        self.__message = message
        self.__filename = filename
        self.__linenum = linenum
    def __str__(self):
        string = 'Error parsing file \"%s\":%s : %s' % (self.__filename,self.__linenum,self.__message)
        return string

AtomListSymbol=0
AtomListId=1
AtomListBondId=2
AtomListBondValue=3
AtomListAngleId=4
AtomListAngleValue=5
AtomListDihedralId=6
AtomListDihedralValue=7

class ZMatrixParser:
    """
    initialize the class.
    The requested format for the zmatrix is
    
    [parameters]
    key=value
    [zmatrix distance_unit="AU" angle_unit="deg"]
    AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]
    [basis]
    identifier basis-string
    AtomSymbol basis-string
    * basis-string
    [symmetry]
    symmetry elements
    
    the [parameters] section is optional. It defines the values for parameters
    that will be used in the zmatrix. if a parameter is undeclared, the zmatrix
    parser section reports an error. You can also specify equations.

    the [zmatrix] section is mandatory, and holds the zmatrix with this format

        AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]

    You can use X as an atomsymbol for the dummy atom. It will be removed from
    the final output.

    the [basis] section is optional, and declares the basis set to use for each
    atom. per default, the numerical identifier is needed. If the AtomSymbol 
    is given, the basis set is assigned to all the atoms with that atomic
    symbol. If the special key * is given, the basis set is assigned to all te
    atoms. Be warned that there's a priority, higher at the top line. If you assign
    the basis A to the identifier 1, the subsequent "*" keyword assigns the basis
    B to all the atoms except the one with identifier 1, which preserves the
    already assigned basis.

    [symmetry] section specifies the symmetry elements expected in the molecule.
    The input requests a single line with space separated keys, where keys are 
    x,y,z for yz,xz and xy reflection planes respectively, xy xz yz for the 
    rotation axis with respect to the z,y,x axis and xyz denotes the inversion.
    """

    def __init__(self): # fold>>
        pass
    # <<fold
    def parseFile(self,infile): # fold>>
        self._infile = FileReader.FileReader(infile)
        self._parameters=_parseParametersSection(self._infile)
        self._zmatrix, self._distance_units, self._angle_units = _parseZMatrixSection(self._infile, self._parameters)
        self._basis=_parseBasisSection(self._infile, self._zmatrix)
        self._symmetries=_parseSymmetrySection(self._infile)
    # <<fold 
    def cartesianCoords(self): # fold>>
        return _cartesianCoords(self._zmatrix, self._basis)
    # <<fold
    def distanceUnits(self): # fold>>
        return self._distance_units
    # <<fold
    def symmetries(self): # fold>>
        return self._symmetries
    # <<fold

def _parseParametersSection(f): # fold>>
    parameters={}
    f.toBOF()
    f.findString("[parameters")
    if f.isAtEOF():
        # no parameter section
        return
    # this re search for key = anything
    regexp = re.compile("^\s*([a-zA-Z]\w*)\s*=\s*(.*)\s*$")
    line = f.readline()
    while not (f.isAtEOF() or line[0] == '['):
        line=string.strip(line)
        if line == '' or line[0] == "#":
            line = f.readline()
            continue
        match = regexp.match(line)
        if match != None:
            val = match.group(2)
            val = _computeParameters(val,parameters)
            val = str(eval(val))
            parameters[match.group(1)] = val
        line = f.readline()
    
    return parameters
# <<fold
def _computeParameters(line, parameters): # fold>>
    notseparators=re.compile('[A-Za-z0-9_]')
    for k,v in parameters.items():
        # find the key in our line
        pos=line.find(k)
        if pos >= 0:
            if pos == 0:
                leftsep=''
            else:
                leftsep=line[pos-1]
            if pos + len(k) == len(line):
                rightsep = ''
            else:
                rightsep = line[pos+len(k)]
            m=notseparators.match(leftsep)
            if m != None:
                continue
            m=notseparators.match(rightsep)
            if m != None:
                continue
            # ok... left and right separators are real separators
            # substitute
            line=line[0:pos]+v+line[pos+len(k):]
    return line
# <<fold
def _parseZMatrixSection(f, parameters): # fold>>
    zmatrix=[]
    currentRead=0

    f.toBOF()
    f.findString("[zmatrix")
    if f.isAtEOF():
        raise ParseError('Unable to find [zmatrix] section ',f.currentPos()+1)

    line = f.currentLine()
    m=re.search("distance_unit\s*=\s*\"([A-Za-z]+)\"", line)
    if m is None:  
        raise ParseError("Unable to find distance_unit specification in [zmatrix] entry. Don't forget the quotes!")


    if m.group(1) in ["Angstrom", "Ang", "angstrom"]:
        distance_unit=Units.angstrom
    elif m.group(1) in ["AtomicUnits", "AU", "Bohr", "bohr"]:
        distance_unit=Units.bohr
    else:
        raise ParseError("Invalid distance_unit specification in [zmatrix] entry. Accepted \"angstrom\" or \"AtomicUnits\". Don't forget quotes!")

    m=re.search("angle_unit\s*=\s*\"([A-Za-z]*)\"", line)
    if m is None:  
        raise ParseError("Unable to find distance_unit specification in [zmatrix] entry")

    if m.group(1) in ["degrees", "deg"]:
        angle_unit = Units.degrees
    elif m.group(1) in ["radians", "rad"]:
        angle_unit = Units.radians
    else:
        raise ParseError("Invalid distance_unit specification in [zmatrix] entry. Accepted \"deg\" or \"rad\". Don't forget quotes!")

    line = f.readline()
    # AtomSymbol IdentifierNum [id distance [id angle [id dihedral]]]
    while not (f.isAtEOF() or line[0] == '['):
        line=string.strip(line)
        if line == '' or line[0] == "#":
            # the line is empty or a comment... skip
            line = f.readline()
            continue
        currentRead=currentRead+1

        # call the replacement function. It replaces occurences of parameters into the
        # zmatrix. btw.. what about this sub into the parameters list itself?

        line = _computeParameters(line,parameters)

        elems=line.split()
        expectedElems=currentRead*2
        if expectedElems > 8:
            expectedElems = 8

        if len(elems) != expectedElems:
                print line
                raise ParseError('Wrong format. Expected elements %d found %d' % (expectedElems, len(elems)),"f.name",f.currentPos()+1)

        # parse the consistency of the line
        # does the atomtype exists?
        if PeriodicTable.getElementBySymbol(elems[AtomListSymbol]) == None:
            raise ParseError('Unknown atom type %s' % elems[AtomListSymbol],"f.name",f.currentPos()+1)
        
        # the current identifier must match the currentRead parameter
        try:
            theid=int(elems[AtomListId])
        except ValueError:
            raise ParseError('Non integer value as id at field 2' ,"f.name",f.currentPos()+1)

        if int(elems[AtomListId]) != currentRead:
            raise ParseError('Error in identifier. Expected %d, found %d.' % (currentRead, int(elems[AtomListId])),"f.name",f.currentPos()+1)

        # for each identifier check if its' integer and lower than the
        # current identifier num (but greater than one! :)), and also if
        # the associated data is numeric
        temp=[]
        for i in range(2,expectedElems,2):
            try:
                theid=int(elems[i])
            except ValueError:
                raise ParseError('Non integer value as id at field %d' % (i+1) ,"f.name",f.currentPos()+1)
            
            # check if there's no duplicated id in this line
            try:
                temp.index(theid)
            except ValueError:
                pass
            else:
                raise ParseError('Duplicated id at field %d' % (i+1) ,"f.name",f.currentPos()+1)
            
            temp.append(theid)
            
            try:
                theval=float(elems[i+1])
            except ValueError:
                raise ParseError('Non numeric value given as parameter at field %d' % (i+2), "f.name",f.currentPos()+1)
            
            if theid < 1 or theid >= currentRead:
                raise ParseError('Wrong id parameter at field %d' % (i+1), "f.name",f.currentPos()+1)
            
        
        
        # ok... the line seems valid.
        # Pack the line in a tuple and add to an array
        
        zmatrix.append(tuple(elems))
        #print tuple(elems)
        
        # new line and restart
        line = f.readline()
    
    return zmatrix, distance_unit, angle_unit
# <<fold
def _parseBasisSection(f, zmatrix): # fold>>
    """
    returns a dictionary containing the basis as a value to every element symbol (key)
    """
    basis={}
    f.toBOF()
    f.findString("[basis")
    if f.isAtEOF():
        # no basis section
        return
    
    regexp1 = re.compile("^\s*(\d*)\s+(.*)\s*$")
    regexp2 = re.compile("^\s*([a-zA-Z]\w*)\s+(.*)\s*$")
    regexp3 = re.compile("^\s*"+re.escape("*")+"\s+(.*)\s*$")
    line = f.readline()
    while not (f.isAtEOF() or line[0] == '['):
        line=string.strip(line)
        if line == '' or line[0] == "#":
            line = f.readline()
            continue
        match1 = regexp1.match(line)
        match2 = regexp2.match(line)
        match3 = regexp3.match(line)
        if match1 != None: # the assignment to an id
            theid = int(match1.group(1))
            if theid > len(zmatrix) or theid < 1:
                raise ParseError('Wrong id parameter %d' % int(theid), "f.name",f.currentPos()+1)
            if not basis.has_key(theid):
                basis[theid]=match1.group(2)
        elif match2 != None:
            theatom = match2.group(1)
            l=[]
            for atom in zmatrix:
                if atom[AtomListSymbol].lower() == theatom.lower():
                    l.append(int(atom[AtomListId]))
            for i in l:
                if not basis.has_key(i):
                    basis[i]=match2.group(2)
        elif match3 != None:
            #print "matched all"
            for i in xrange(1,len(zmatrix)+1):
                if not basis.has_key(i):
                    basis[i]=match3.group(1)
        line = f.readline()
    return basis
# <<fold
def _parseSymmetrySection(f): # fold>>
    check=['X','Y','Z','XY','XZ','YZ','XYZ']
    f.toBOF()
    f.findString("[symmetry")
    if f.isAtEOF():
        # no symmetry section
        return None

    line=f.readline()
        
    while not (f.isAtEOF() or line[0] == '['):
        line=string.strip(line)
        if line == '' or line[0] == "#":
            line = f.readline()
            continue
        symmetries=line.upper().split()

        for k in symmetries:
            if k not in check:
                raise ParseError('Unknown symmetry key %s' % k, "f.name",f.currentPos()+1)
        line=f.readline()

    return symmetries
# <<fold
def _cartesianCoords(zmatrix, basis): # fold>>
    cart=[]
    
    for currentAtom in zmatrix:
        carttmp=[]
        if zmatrix.index(currentAtom) == 0:
            # first atom, place in the center
            if basis.has_key( int(currentAtom[AtomListId]) ):
                _basis = basis[ int(currentAtom[AtomListId] ) ]
            else:
                _basis = ''
            #print '-> _basis ',_basis,' ', int(currentAtom[AtomListId]) 
            cart.append( (currentAtom[AtomListSymbol], Math.Vector3(0.0,0.0,0.0),  _basis))
        elif zmatrix.index(currentAtom) == 1:
            # the second atom. Place along the z axis at the bond distance
            if basis.has_key( int(currentAtom[AtomListId]) ):
                _basis = basis[ int(currentAtom[AtomListId] ) ]
            else:
                _basis = ''
            #print '-> _basis ',_basis,' ', int(currentAtom[AtomListId]) 
            cart.append( (currentAtom[AtomListSymbol], Math.Vector3(0.0, 0.0, float(currentAtom[AtomListBondValue])), _basis))
        elif zmatrix.index(currentAtom) == 2:
            # {{{
            # third atom. copy into a temporary buffer the cart position of 1 and 2
            # WARNING: atom 1 for zmatrix enumeration is element 0 in the cartesian list
            # so always decrease indexes by one. Also remember that zmatrix storagement is
            # per-string. Id's are strings, distances and angles too... always convert to
            # int or float to manage
            idx = int(currentAtom[AtomListBondId])-1
            carttmp.append( copy.deepcopy(cart[idx]) )
            idx = int(currentAtom[AtomListAngleId])-1
            carttmp.append( copy.deepcopy(cart[idx]) ) 
            # center the bond reference angle
            # now carttmp holds:
            # in position 0 the bond lenght reference atom
            # in position 1 the angle reference atom

            # choose the first atom and set as the center of the world
            # create a new tuple object with the cartesian parameters

            firstAtom=carttmp[0]
            firstAtomCoords=firstAtom[1]
            secondAtom=carttmp[1]
            secondAtomCoords=secondAtom[1]
            newcenter = (firstAtomCoords.x(), firstAtomCoords.y(), firstAtomCoords.z())
            # remember: newcenter is a tuple for xyz

            # translate each atom by carttmp
            for atom in carttmp:
                atom[1].translate(-newcenter[0],-newcenter[1],-newcenter[2])

            # keep the translated transformation, to revert it later

            translation=(newcenter[0],newcenter[1],newcenter[2])

            # done... now carttmp holds the translated elements.
            # please note that firstAtom and secondAtom are a reference in the
            # list carttmp, so they get updated too.
            # now work on the second atom, rotate the whole carttmp so to have
            # the second atom on z

            # the length of zy
            ryz=math.sqrt(secondAtomCoords.y()**2+secondAtomCoords.z()**2)
            if ryz > 1e-10:
                # the cosine of the angle
                rapp=secondAtomCoords.z()/ryz
                # choose the correct quadrant
                sign=1
                if secondAtomCoords.y() < 0:
                    sign=-1
                xangle=sign*math.acos(rapp)
            else:
                if secondAtomCoords.y() < 0:
                    xangle=math.pi
                else:
                    xangle=0.0
                
            # now rotate along x
            for atom in carttmp[:]:
                atom[1].rotateX(-xangle)

            # do the same on the y axis
            # the lenght of xz
            rxz=math.sqrt(secondAtomCoords.x()**2+secondAtomCoords.z()**2)

            if rxz > 1e-10 :
                # the cosine of the angle
                rapp=secondAtomCoords.z()/rxz
                # choose the correct quadrant
                sign=1
                if secondAtomCoords.x() < 0:
                    sign=-1
                yangle=sign*math.acos(rapp)
            else:
                if secondAtomCoords.x() < 0:
                    yangle=math.pi
                else:
                    yangle=0.0

            # now rotate along y
            for atom in carttmp:
                atom[1].rotateY(-yangle)
            
            # keep the rotation transformation close at hand, to revert it later
            rotation=(xangle, yangle, 0.0)
            
            # it's time to place our new atom

            vec=Math.Vector3(0.0, 0.0, float(currentAtom[AtomListBondValue]))
            angle=float(currentAtom[AtomListAngleValue])*math.pi/180
            vec.rotateX(angle)
            
            # ok.. time to backtransform and regain the position against the
            # original system. Rotate only the current atom vector, since
            # we no longer care about the other atoms.

            vec.rotateY(rotation[1])
            vec.rotateX(rotation[0])
            vec.translate(translation[0],translation[1],translation[2])

            # time to add the atom to our cartesian list
            if basis.has_key( int(currentAtom[AtomListId]) ):
                _basis = basis[ int(currentAtom[AtomListId] ) ]
            else:
                _basis = ''
            #print '-> _basis ',_basis,' ', int(currentAtom[AtomListId]) 
            cart.append( (currentAtom[AtomListSymbol], vec, _basis))
            # }}}
        elif zmatrix.index(currentAtom) >= 3:
            # {{{
            # ok... the same as for index = 2, plus the dihedral rotation
            # cut and paste of the previous section, stripped of the comments
            # should we merge with the previous case ?
            idx = int(currentAtom[AtomListBondId])-1
            carttmp.append( copy.deepcopy(cart[idx]) )
            idx = int(currentAtom[AtomListAngleId])-1
            carttmp.append( copy.deepcopy(cart[idx]) ) 

            # add the dihedral reference angle
            idx = int(currentAtom[AtomListDihedralId])-1
            carttmp.append( copy.deepcopy(cart[idx]) ) 

            # now carttmp holds:
            # in position 2 the dihedral reference atom

            firstAtom=carttmp[0]
            firstAtomCoords=firstAtom[1]
            secondAtom=carttmp[1]
            secondAtomCoords=secondAtom[1]
            thirdAtom=carttmp[2]
            thirdAtomCoords=thirdAtom[1]
            newcenter = (firstAtomCoords.x(), firstAtomCoords.y(), firstAtomCoords.z())

            for atom in carttmp:
                atom[1].translate(-newcenter[0],-newcenter[1],-newcenter[2])

            translation=(newcenter[0],newcenter[1],newcenter[2])

            ryz=math.sqrt(secondAtomCoords.y()**2+secondAtomCoords.z()**2)
            if ryz > 1e-10:
                rapp=secondAtomCoords.z()/ryz
                sign=1
                if secondAtomCoords.y() < 0:
                    sign=-1
                xangle=sign*math.acos(rapp)
            else:
                if secondAtomCoords.y() < 0:
                    xangle=math.pi
                else:
                    xangle=0.0
                
            for atom in carttmp:
                atom[1].rotateX(-xangle)

            rxz=math.sqrt(secondAtomCoords.x()**2+secondAtomCoords.z()**2)

            if rxz > 1e-10 :
                rapp=secondAtomCoords.z()/rxz
                sign=1
                if secondAtomCoords.x() < 0:
                    sign=-1
                yangle=sign*math.acos(rapp)
            else:
                if secondAtomCoords.x() < 0:
                    yangle=math.pi
                else:
                    yangle=0.0

            for atom in carttmp:
                atom[1].rotateY(-yangle)
            # now we need to rotate the atoms along the z axis so the third
            # atom is on the yz plane

            rxy=math.sqrt(thirdAtomCoords.x()**2+thirdAtomCoords.y()**2)
            if rxy > 1e-10 :
                rapp=thirdAtomCoords.y()/rxy
                sign=1
                if thirdAtomCoords.x() < 0:
                    sign=-1
                zangle=sign*math.acos(rapp)
            else:
                raise ParseError('Third atom %d is collinear with %d and %d at specification for atom %d' % (int(currentAtom[AtomListDihedralId]), int(currentAtom[AtomListBondId]), int(currentAtom[AtomListAngleId]), int(currentAtom[AtomListId])) ,None,None)

            for atom in carttmp:
                atom[1].rotateZ(-zangle)
            
            rotation=(xangle, yangle, zangle)

            # it's time to place our new atom

            vec=Math.Vector3(0.0, 0.0, float(currentAtom[AtomListBondValue]))
            angle=float(currentAtom[AtomListAngleValue])*math.pi/180
            vec.rotateX(angle)
            angle=float(currentAtom[AtomListDihedralValue])*math.pi/180
            vec.rotateZ(angle)

            vec.rotateZ(rotation[2])
            vec.rotateY(rotation[1])
            vec.rotateX(rotation[0])
            vec.translate(translation[0],translation[1],translation[2])
            if basis.has_key( int(currentAtom[AtomListId]) ):
                _basis = basis[ int(currentAtom[AtomListId] ) ]
            else:
                _basis = ''
            #print '-> basis ',basis,' ', int(currentAtom[AtomListId]) 

            cart.append( (currentAtom[AtomListSymbol], vec, _basis))

    return cart

# <<fold

