import re
from theochempy._theochempy import Measure
from theochempy._theochempy import Units
from theochempy._theochempy.Chemistry import PeriodicTable

__all__ = ['ParseError', 'XYZFile']

class ParseError(Exception): pass

class Molecule:
    def __init__(self):
        self.comment = None
        self.atom_list = []

class XYZFile:

    def __init__(self, filename = None):
        self._filename = filename
        self._molecules = []

        if filename is None:
            return

        f=file(self._filename,"r")
       
        STATE_START, STATE_NUM_ATOMS, STATE_COMMENT, STATE_ATOM_ROW = range(4)

        state = STATE_START 

        for line_num, line in enumerate(f):
            m = re.search("^\s*\d+\s*$", line)
            if m is not None:
                if state == STATE_START or state == STATE_ATOM_ROW:
                    current_molecule = Molecule()
                    self._molecules.append(current_molecule)
                    state = STATE_NUM_ATOMS
                    continue
                else:
                    raise ParseError("Found number of atoms at invalid position, line %d, file %s. " % (line_num, filename))
                    

            m = re.search("^\s*([A-Z]+[a-z]*[a-z]*)\s+(-?\d*\.\d+)\s*(-?\d*\.\d+)\s*(-?\d*\.\d+)\s+$", line)
            if m is not None:
                if state == STATE_COMMENT or state == STATE_ATOM_ROW:
                    element = PeriodicTable.getElementBySymbol(m.group(1))
                    if element is None:
                        raise ParseError("Invalid element symbol %s at line %d, file %s" % (m.group(1), line_num, filename))
                    
                    position = Measure.Measure( ( float(m.group(2)), float(m.group(3)), float(m.group(4))), Units.angstrom )

                    current_molecule.atom_list.append( (element, position) )
                    state = STATE_ATOM_ROW
                    continue
                else:
                    raise ParseError("Found atom line at invalid position, line %d, file %s. " % (line_num, filename))
                
            m = re.search("^\s*.*\s*$", line)
            if m is not None:
                if state == STATE_NUM_ATOMS:
                    current_molecule.comment = line.strip()
                    state = STATE_COMMENT
                    continue
                else:
                    raise ParseError("Found comment line at invalid position, line %d, file $s. " % (line_num, filename))
        
        f.close()
        
    def comment(self, molecule_index=-1):
        if len(self._molecules) == 0:
            return None
        return self._molecules[molecule_index].comment

    def numOfMolecules(self):
        return len(self._molecules)

    def numOfAtoms(self, molecule_index=-1):
        if len(self._molecules) == 0:
            return None
        return len(self._molecules[molecule_index].atom_list)

    def atom(self, *args):
        if len(args) == 1:
            atom_index = args[0]
            molecule_index = -1
        elif len(args) == 2:
            molecule_index = args[0]
            atom_index = args[1]
        else:
            raise TypeError("Invalid number of arguments %d" % len(args))

        if len(self._molecules) == 0:
            return None
        return self._molecules[molecule_index].atom_list[atom_index]


    def createMolecule(self, molecule_index=None):
        current_molecule = Molecule()

        if molecule_index is None:
            self._molecules.append(current_molecule)
            return len(self._molecules)-1
        else:
            self._molecules.insert(molecule_index, current_molecule)
            return molecule_index

     
    def setComment(self, *args):
        if len(args) == 1:
            comment = args[0]
            molecule_index = -1
        elif len(args) == 2:
            molecule_index = args[0]
            comment = args[1]
        else: 
            raise TypeError("Invalid number of arguments %d" % len(args))

        self._molecules[molecule_index].comment = comment
        

    def addAtom(self, *args):
        if len(args) == 1:
            atom = args[0]
            molecule_index = -1
        elif len(args) == 2:
            molecule_index = args[0]
            atom = args[1]
        else:
            raise TypeError("Invalid number of arguments %d" % len(args))

        self._molecules[molecule_index].atom_list.append(atom)

    def setAtom(self, *args):
        if len(args) == 2:
            atom_index = args[0]
            atom = args[1]
            molecule_index = -1
        elif len(args) == 2:
            molecule_index = args[0]
            atom_index = args[1]
            atom = args[2]
        else:
            raise TypeError("Invalid number of arguments %d" % len(args))
        self._molecules[molecule_index].atom_list[atom_index] = atom

    def saveTo(self, filename):
        f = file(filename, "w")
        for molecule in self._molecules:
            f.write(" %d\n" % len(molecule.atom_list))
            f.write("%s\n" % molecule.comment)
            for atom in molecule.atom_list:
                element, coordinate = atom
                coordinate_angstromg = coordinate.asUnit(Units.angstrom)
                f.write("%s  %20.10f %20.10f %20.10f\n" % (element.symbol(), coordinate_angstromg.value()[0], coordinate_angstromg.value()[1], coordinate_angstromg.value()[2]))

        f.close()
