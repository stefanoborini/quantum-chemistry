from theochempy._theochempy import Measure
from theochempy._theochempy import Units

import numpy
import re
import string

class HeaderDissociatedToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("List of Dissociated Structures")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        reader.toPos(start_pos)
        return None 
        # <<fold

class HeaderEquilibriumToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("List of Equilibrium Structures")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        reader.toPos(start_pos)
        return None 
        # <<fold

class HeaderTransitionToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("List of Transition Structures")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        reader.toPos(start_pos)
        return None 
        # <<fold

class StructureHeaderToken:
    def __init__(self, type, number, symmetry): #  fold>>
        self._type = type
        self._number = number
        self._symmetry = symmetry
    # <<fold
    def type(self): # fold>>
        return self._type
    # <<fold
    def number(self): # fold>>
        return self._number
    # <<fold
    def symmetry(self): # fold>>
        return self._symmetry
    # <<fold
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        
        m = re.search("# Geometry of (\S+) (\d+), SYMMETRY = (\S+)", line)

        if m is None:

            reader.toPos(start_pos)
            return None
        return cls( type=m.group(1), number=int(m.group(2)), symmetry=m.group(3))
    # <<fold


class GeometryToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()
        atom_list = []

        valid_data = False
        for line in reader:
     
            m1 = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m1 is not None:
                atom_label = m1.group(1)
                position = Measure.Measure( (float(m1.group(2)),
                                             float(m1.group(3)),
                                             float(m1.group(4))
                                             ), Units.angstrom
                                            )
                atom_list.append( (atom_label, position) )
                valid_data = True
                continue

            break
       
        reader.readbackline()
        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            reader.toPos(start_pos)
            return None

        return cls(atom_list)

    # <<fold 


class EnergyToken:
    def __init__(self, energy): #  fold>>
        self._energy = energy
        # <<fold
    def energy(self): # fold>>
        return self._energy
        # <<fold 
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("Energy\s+=\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( Measure.Measure( float(m.group(1)), Units.hartree ))

        reader.toPos(start_pos)
        return None
    # <<fold


class SpinToken:
    def __init__(self, spin): #  fold>>
        self._spin = spin
        # <<fold
    def spin(self): # fold>>
        return self._spin
        # <<fold 
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+=\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( Measure.Measure( float(m.group(1)), Units.unknown ))

        reader.toPos(start_pos)
        return None
    # <<fold

class ZPVEToken:
    def __init__(self, zpve): #  fold>>
        self._zpve = zpve
        # <<fold
    def zpve(self): # fold>>
        return self._zpve
        # <<fold 
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("ZPVE\s+=\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( Measure.Measure( float(m.group(1)), Units.unknown ))

        reader.toPos(start_pos)
        return None
    # <<fold


class NormalModesToken:
    def __init__(self, eigenvalues): # fold>>
        self._eigenvalues = eigenvalues
    def eigenvalues(self):
        return self._eigenvalues
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        eigenvalues = []
        
        m = re.search("Normal mode eigenvalues : nmode = (\d+)", line)
        if m is None:
            reader.toPos(start_pos)
            return None

        num_of_eigenvalues = int(m.group(1))

        num_of_full_lines = int(num_of_eigenvalues / 5)
        remainder = num_of_eigenvalues % 5


        for i in xrange(num_of_full_lines):
            line = reader.readline()
            m1 = re.search("(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)", line)
            if m1 is None:
                reader.toPos(start_pos)
                return None
            for j in xrange(1,6):
                eigenvalues.append(float(m1.group(j)))

        if remainder != 0:
            m2 = re.search("\s+".join(["(-?\d*\.\d*)"]*remainder), line)
            if m2 is None:
                reader.toPos(start_pos)
                return None
            for i in xrange(1,remainder+1):
                eigenvalues.append(float(m1.group(j)))
    
        return cls(eigenvalues)
        # <<fold 
# <<fold            

class ConnectionToken:
    def __init__(self, first, second): #  fold>>
        self._first = first
        self._second = second
        # <<fold
    def first(self): # fold>>
        return self._first
        # <<fold 
    def second(self): # fold>>
        return self._second
        # <<fold 
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("CONNECTION : (\S+) - (\S+)", line)
        if m is not None:
            return cls( m.group(1), m.group(2))

        reader.toPos(start_pos)
        return None
    # <<fold




def fullGrammar():
    token_grammar=[ 
            HeaderDissociatedToken,
            HeaderEquilibriumToken,
            HeaderTransitionToken,
            StructureHeaderToken,
            GeometryToken,
            EnergyToken,
            SpinToken,
            ZPVEToken,
            NormalModesToken,
            ConnectionToken,
            ] 
    return token_grammar


