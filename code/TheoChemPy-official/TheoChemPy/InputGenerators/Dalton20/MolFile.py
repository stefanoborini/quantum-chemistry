from TheoChemPy import Units
import StringIO
import string

class MolFile:
    def __init__(self):
        self.__atom_list= []
        self.__force_atom_basis=False
        self.__comment_1 = ""
        self.__comment_2 = ""
        self.__symmetry_generators = None
    def forceAtomBasis(self, force):
        self.__force_atom_basis = force
    def addComment(self, line1, line2): 
        self.__comment_1 = line1
        self.__comment_2 = line2
        pass
    def addAtom(self, label, element, coords, unit, basis_set): 
        self.__atom_list.append( (label, element, coords, unit, basis_set) )
    def setSymmetryGenerators(self, generators):
        self.__symmetry_generators = generators
    def generateOutput(self):
        """
        this routine prints the dalton .mol format for the given molecule
        in dalton 2.0 format
        """
        data = StringIO.StringIO()

        used_basis_sets = set(map(lambda x: x[4], self.__atom_list))

        if len(used_basis_sets) == 1 and not self.__force_atom_basis:
            one_basis_set = True
        else:
            one_basis_set = False

        if one_basis_set:
            data.write("BASIS\n")
            data.write("%s\n" % ( list(used_basis_sets)[0] ,))
        else:
            data.write("ATOMBASIS\n")

        data.write(self.__comment_1[0:80]+"\n")
        data.write(self.__comment_2[0:80]+"\n")

        groups={}
        for atom in self.__atom_list:
            element = atom[1]
            basis = atom[4]
            key = (element,basis)
            if not groups.has_key(key):
                groups[key]=[]
            groups[key].append(atom)

        used_units = set(map(lambda x: x[3], self.__atom_list))
        if len(used_units) == 1:
            one_unit = True
            if list(used_units)[0] == Units.Angstrom:
                unit_string = "Angstrom"
            elif list(used_units)[0] == Units.Bohr:
                unit_string = ""
            else:
                raise Exception("Invalid unit used")
        else:
            one_unit = False
            raise Exception("Invalid data found. Please use homogeneous units for now")

        if self.__symmetry_generators is not None:
            generators_string = "Generators=%d %s\n" % (len(self.__symmetry_generators), string.join(self.__symmetry_generators).upper())
        else:
            generators_string = ""

        data.write( 
            string.strip(
                string.join(
                    [unit_string,"Atomtypes="+str(len(groups.keys())), generators_string]
                    )
                )+"\n"
            )

        for key,atomList in groups.items():
            element, basis = key 
            if one_basis_set:
                data.write( "Charge=%d.0 Atoms=%d\n" % (element.atomicNumber(), len(atomList)))
            else:
                data.write( "Charge=%d.0 Atoms=%d Basis=%s\n" % (element.atomicNumber(), len(atomList), basis))
            currentatom = 0
            for atom in atomList:
                data.write( '%-4s  %10.6f  %10.6f  %10.6f\n' % (atom[0], atom[2][0], atom[2][1], atom[2][2]) )

        data.pos = 0 
        return data.read()
    # <<fold 

