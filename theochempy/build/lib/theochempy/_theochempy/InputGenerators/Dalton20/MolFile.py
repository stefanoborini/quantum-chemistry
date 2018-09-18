from theochempy._theochempy import Units
import StringIO
import string


class Group:
    def __init__(self, element, basis):
        self._element = element
        self._basis = basis
        self._atom_list = []

    def appendAtom(self, label, coords):
        """accepts a tuple containing:

        """
        self._atom_list.append( (label, coords) )

    def element(self):
        return self._element
    def basis(self):
        return self._basis

    def toText(self, use_atombasis):
        data = StringIO.StringIO()
        if use_atombasis:
            data.write( "Charge=%d.0 Atoms=%d Basis=%s\n" % (self._element.atomicNumber(), len(self._atom_list), self._basis))
        else:
            data.write( "Charge=%d.0 Atoms=%d\n" % (self._element.atomicNumber(), len(self._atom_list)))

        for atom in self._atom_list:
            label, coords = atom
            data.write( '%-4s  %20.10f  %20.10f  %20.10f\n' % (label, coords.value()[0], coords.value()[1], coords.value()[2]) )
        data.pos=0
        return data.read()

class MolFile:
    """A class representing a Dalton 2.0 mol file.
    You can generate this file by providing programmatic information by means of the
    provided methods, and finally generate the result by means of the generateOutput method
    """
    def __init__(self): # fold>>
        """Initializes the MolFile class
        """
        self.__atom_list= []
        self.__force_atom_basis=False
        self.__comment_1 = ""
        self.__comment_2 = ""
        self.__symmetry_generators = None
        # <<fold
    def forceAtomBasis(self, force): # fold>>
        """Forces the use of the ATOMBASIS keyword, assigining the basis sets
        to each group of atoms even if all of them have the same basis

        @param force : a boolean. if True, ATOMBASIS is used.
        @return None
        """
        self.__force_atom_basis = force
        # <<fold
    def addComment(self, line1, line2):  # fold>>
        self.__comment_1 = line1
        self.__comment_2 = line2
        # <<fold
    def addAtom(self, label, element, coords, basis):  # fold>>
        """Adds an atom.

        @param label : a string label assigned to the atom
        @param element : an element class from the periodic table module
        @param coords : the coordinates as a Measure
        @param basis : the basis set name, as a string
        @return None
        """
        self.__atom_list.append( (label, element, coords, basis) )
    # <<fold
    def setSymmetryGenerators(self, generators): # fold>>
        """Sets the symmetry generators

        @param generators: a list of strings, each one representing one generator.
        @return None
        """
        self.__symmetry_generators = generators
        # <<fold
    def generateOutput(self): # fold>>
        """
        Prints the dalton .mol format for the given molecule in dalton 2.0
        format

        @return a string containing the generated output
        """
        data = StringIO.StringIO()

        used_basis = set(map(lambda x: x[3], self.__atom_list))

        if len(used_basis) == 1 and not self.__force_atom_basis:
            use_atombasis = False
        else:
            use_atombasis = True

        if use_atombasis:
            data.write("ATOMBASIS\n")
        else:
            data.write("BASIS\n")
            data.write("%s\n" % ( list(used_basis)[0] ,))

        data.write(self.__comment_1[0:80]+"\n")
        data.write(self.__comment_2[0:80]+"\n")

        group_list = []
        for atom in self.__atom_list:
            label, element, coords, basis = atom
            group_filter = filter(lambda x: x.basis() == basis and x.element() == element, group_list)
            if len(group_filter) == 0:
                group = Group(element, basis)
                group_list.append(group)
            else:
                group = group_filter[0]

            group.appendAtom(label, coords)

        if len(group_list) == 0:
            raise Exception("No atoms specified")

        used_units = set(map(lambda x: x[2].unit(), self.__atom_list))
        if len(used_units) == 1:
            one_unit = True
            if list(used_units)[0] == Units.angstrom:
                unit_string = "Angstrom"
            elif list(used_units)[0] == Units.bohr:
                unit_string = ""
            else:
                raise Exception("Invalid unit used")
        else:
            raise Exception("Invalid data found. Please use homogeneous units for now")

        if self.__symmetry_generators is not None:
            generators_string = "Generators=%d %s\n" % (len(self.__symmetry_generators), string.join(self.__symmetry_generators).upper())
        else:
            generators_string = ""

        data.write( 
            string.strip(
                string.join(
                    [unit_string,"Atomtypes="+str(len(group_list)), generators_string]
                    )
                )+"\n"
            )

        group_list = sorted(group_list, key=lambda x : x.element().atomicNumber() )
        for group in group_list:
            data.write(group.toText(use_atombasis))

        data.pos = 0 
        return data.read()
    # <<fold 

