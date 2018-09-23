from theochempy._theochempy import Measure
from theochempy._theochempy import Units

import numpy
import re
import string

class CommandDirectiveToken:
    def __init__(self, command_line, job_string, method_string, basis_set_string) : # fold>>
        self._command_line = command_line
        self._job_string = job_string
        self._method_string = method_string
        self._basis_set_string = basis_set_string
    # <<fold
    def commandLine(self):
        return self._command_line
    def jobString(self):
        return self._job_string
    def methodString(self):
        return self._method_string
    def basisSetString(self):
        return self._basis_set_string
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("^#\s+(.*)$")
        line = reader.readline()
        m1 = regexp.search(line)
        if m1 is not None:
            command_line = m1.group(1)
            parts = command_line.split("/") 
            if len(parts) != 3:
                reader.toPos(start_pos)
                return None

            return cls(command_line, parts[0], parts[1], parts[2])

        reader.toPos(start_pos)
        return None 
        # <<fold

class GeometryToken:
    def __init__(self, atom_list, charge, spin): # fold>>
        self._atom_list = atom_list
        self._charge = charge
        self._spin = spin
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    def charge(self): # fold>>
        return self._charge
    # <<fold
    def spin(self): # fold>>
        return self._spin
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()
        atom_list = []

        valid_data = False
        for line in reader:
            m0 = re.search("^(\d)\s+(\d)\s*$", line)
            if m0 is not None:
                charge = int(m0.group(1))
                spin = int(m0.group(2))
                continue

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

        return cls(atom_list, charge, spin)

    # <<fold 

class OptionsHeaderToken:
    def __init__(self) : # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        if line.strip().lower() == "options":
            return cls()

        reader.toPos(start_pos)
        return None 
        # <<fold

class NRunOptionToken:
    def __init__(self, value): #  fold>>
        self._value = value
        # <<fold
    def value(self): # fold>>
        return self._value
        # <<fold 
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("(\w*?)\s+=\s+(\d+)", line)
        if m is not None:
            if m.group(1).strip().lower() == "nrun":
                return cls(int(m.group(2)))

        reader.toPos(start_pos)
        return None
    # <<fold



def fullGrammar():
    token_grammar=[ 
            CommandDirectiveToken,
            GeometryToken,
            OptionsHeaderToken,
            NRunOptionToken,
            ] 
    return token_grammar


