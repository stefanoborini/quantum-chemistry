#/usr/bin/env python
# @author Stefano Borini
# @description this script extracts the final geometry in a dalton file.
# @description and produces the dalton .mol file
# @description It uses TheoChemPy.
# @license Artistic License 2.0

import os
import sys

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens
from theochempy._theochempy.InputGenerators.Dalton20 import MolFile
from theochempy._theochempy.Chemistry import PeriodicTable
from theochempy._theochempy import Units
from theochempy._theochempy.Molecules import XYZMolecule
from theochempy._theochempy import Measure

import getopt
import numpy



class Options:
    RELABEL_SYMBOL_LETTERS="letters"
    RELABEL_SYMBOL_SUBSCRIPTS="subscripts"

    def __init__(self): # fold>>
        self.dalton_out_filename = None
        self.dalton_mol_filename = None
        self.relabel_symbols=None
        self.align = None
        self.basis = None
    # <<fold
def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "ab:r:h", ["align", "basis=", "relabel-symbols=", "help"])

    for opt in opts:
        if opt[0] == "-a" or opt[0] == "--align":
            options.align=True
        if opt[0] == "-b" or opt[0] == "--basis":
            options.basis = opt[1]
        if opt[0] == "-r" or opt[0] == "--relabel-symbols":
            if opt[1] != Options.RELABEL_SYMBOL_LETTERS and opt[1] != Options.RELABEL_SYMBOL_SUBSCRIPTS:
                _usage()
                sys.exit(1)
            options.relabel_symbols = opt[1]
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)

    if len(args) != 2:
        _usage()
        sys.exit(1)

    if options.align is None:
        options.align = False

    if options.align is False and options.relabel_symbols is not None:
        _usage()
        sys.exit(1)

    if options.align is True and options.relabel_symbols is None:
        options.relabel_symbols = Options.RELABEL_SYMBOL_SUBSCRIPTS

    options.dalton_out_filename = args[0]
    options.dalton_mol_filename = args[1]
    return options
    # <<fold

class Molecule:
    def __init__(self): # fold>>
        self.coordinates_list = []
        self.elements_list = []
        self.symmetries_list = []
        self.labels_list = []
        self.symmetry_generators = None
        self.basis_set = None
        # <<fold
    def createXYZMolecule(self): # fold>>
        atom_list = []
        for element, coords in zip(self.elements_list, self.coordinates_list):
            atom_list.append((element, coords))
        return XYZMolecule.XYZMolecule(atom_list)
        # <<fold
            
class Parser:
    def __init__(self, dalton_out_filename): # fold>>
        token_list = Dalton20.tokenizeOutFile(dalton_out_filename)

        atom_basis_set_token = self._getAtomsAndBasisSetsToken(token_list)
        geometry_token = self._getFinalGeometryToken(token_list)
        symmetry_token = self._getSymmetryToken(token_list)
    
        mol = Molecule()
        mol.symmetry_generators = symmetry_token.generators()
        mol.basis_set = atom_basis_set_token.basisSet()

        for label, symmetry, coords in geometry_token.atomList():
            element = _labelToElement(label, atom_basis_set_token.atomDataList())
            mol.elements_list.append(element)
            mol.labels_list.append(label)
            mol.symmetries_list.append(symmetry)
            mol.coordinates_list.append(coords)

        self._molecule = mol
        # <<fold
    def _getAtomsAndBasisSetsToken(self,token_list): # fold>>
        tokens = filter(lambda x: x.__class__ == Tokens.AtomsAndBasisSetsToken, token_list)
        if len(tokens) != 1:
            raise Exception("Sorry. Could not find atom and basis set information")
        token = tokens[0]
        if token.basisSet() is None:
            raise Exception("Sorry, only single basis set (BASIS) description are currently supported")
        return token
        # <<fold
    def _getFinalGeometryToken(self, token_list): # fold>>
        end_of_optimization = False
        for token in token_list:
            if token.__class__ == Tokens.EndOfOptimizationHeaderToken:
                end_of_optimization = True
    
            if end_of_optimization:
                if token.__class__ == Tokens.FinalGeometryToken:
                    return token
    
        raise Exception("Sorry. Could not find final geometry")
        # <<fold
    def _getSymmetryToken(self, token_list): # fold>>
        tokens = filter(lambda x: x.__class__ == Tokens.SymmetryToken, token_list)
        if len(tokens) != 1:
            raise Exception("Sorry. Could not find symmetry generators")
        return tokens[0]
        # <<fold
    def getMolecule(self): # fold>>
        return self._molecule
    # <<fold


def _labelToElement(find_label, datalist): # fold>>
    for t in datalist:
        label, symmetry, atomic_number, basis_expanded, basis_contracted, basis_string = t
        if label == find_label:
            return PeriodicTable.getElementByAtomicNumber(atomic_number)

    return None
    # <<fold
def _getAlignmentOperations(molecule): # fold>>
    xyz_mol = molecule.createXYZMolecule()
    center_of_mass = XYZMolecule.centerOfMass(xyz_mol)

    xyz_mol.translate(-center_of_mass)
    moments_of_inertia = XYZMolecule.momentsOfInertia(xyz_mol)
    
    # we multiply the eigenvectors by -1 if needed.
    # we want to keep the molecule oriented so that it does not change dramatically
    # (ex. we don't want it to flip just because the diagonalization returned the
    # inertial axis in the other direction)
    v0 = numpy.array(moments_of_inertia[0][1].value())
    if v0[0] < 0.0:
        v0 = -v0
    v1 = numpy.array(moments_of_inertia[1][1].value())
    if v1[1] < 0.0:
        v1 = -v1
    v2 = numpy.array(moments_of_inertia[2][1].value())
    if v2[2] < 0.0:
        v2 = -v2

    rotation = numpy.zeros((3,3))
    rotation[0,0] = v0[0]
    rotation[0,1] = v0[1]
    rotation[0,2] = v0[2]
    rotation[1,0] = v1[0]
    rotation[1,1] = v1[1]
    rotation[1,2] = v1[2]
    rotation[2,0] = v2[0]
    rotation[2,1] = v2[1]
    rotation[2,2] = v2[2]
     
    return (-center_of_mass, rotation)
    # <<fold
def _alignMolecule(molecule, relabel_symbols): #fold>>
    translation_vector, rotation_matrix = _getAlignmentOperations(molecule)
    new_mol = Molecule()

    # the geometry contains all the atoms, even the redundant for symmetry
    # this is how dalton works and how the geometry token works.
    new_coords_list = []
    for coords in molecule.coordinates_list:
        v1 = numpy.array(coords.value())
        v2 = numpy.array(translation_vector.asUnit(coords.unit()).value())
        v3 = v1+v2
        new_coords_list.append(Measure.Measure(numpy.dot(rotation_matrix, v3), coords.unit()))

    new_mol.coordinates_list = new_coords_list
    new_mol.basis_set = molecule.basis_set
    new_mol.symmetry_generators = []
    new_mol.elements_list = molecule.elements_list

    labels_list = []
    symmetries_list = []
    for label, symmetry  in zip(molecule.labels_list, molecule.symmetries_list):
        # after rotation, we technically loose the symmetry, so we cannot store the symmetry label
        # anymore. We must delete it. but this means that now we have two or more atoms
        # with the same label. We add something to the label, but the limit for labels in dalton is 
        # 4 characters. Every character after that will be ignored. so we have to raise an exception if
        # we go out of this limit.
        #
        if symmetry == "": 
            # an unsymmetrical, unique atom
            labels_list.append(label)
        else: 
            # we have a symmetrized atom. we append the symmetry label to its label
            if relabel_symbols == Options.RELABEL_SYMBOL_SUBSCRIPTS:
                label = label+"_"+str(symmetry)
            elif relabel_symbols == Options.RELABEL_SYMBOL_LETTERS:
                label=label+["A","B","C","D","E","F","G","H"][int(symmetry)-1]
            else:
                raise Exception("How the hell did you get here?")
            if len(label) > 4:
                raise Exception("Sorry, atom "+label+" has a label length larger than the allowed 4 in dalton input")
            labels_list.append(label)
        symmetries_list.append("")

    new_mol.labels_list = labels_list
    new_mol.symmetries_list = symmetries_list
    return new_mol
    # <<fold 

def _usage(): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" [--align] [--basis=basis] [--relabel-symbols=sym_spec] dalton_out_filename dalton_mol_filename"
    print ""
    print "--align"
    print "                aligns the molecule so that its center of mass is in the origin, "
    print "                and the rotational axes are aligned along the cartesian axes. "
    print "                The axis with the lower inertial moment will be aligned to the"
    print "                X axis, then Y, then Z."
    print "                Using this option will remove the symmetry, and the produced"
    print "                molfile will contain all the atoms. Labels for symmetry generated"
    print "                atoms will be appended with an underscore, followed by the previous"
    print "                symmetry label. If the resulting label is too long (>4) an error"
    print "                will be returned"
    print ""
    print "--basis=basis"
    print "                overrides the basis set from the file, and replaces it with a common"
    print "                basis set, as specified"
    print ""
    print "--relabel-symbols=sym_spec"
    print "                When align is used, symmetric atoms will become real atoms, due to loss"
    print "                of symmetry. Their labels need to be altered to preserve uniqueness. This"
    print "                option specifies how to alter the names."
    print "                sym_spec can be:"
    print "                   letters    : marked with an additional letter (A,B,C,D). "
    print "                                Ex: C1 1 -> C1A"
    print "                                Ex: C1 2 -> C1B"
    print "                   subscripts : marked with a underscore, followed by the sym number."
    print "                                this is the default."
    print "                                Ex: C1 1 -> C1_1"
    print "                                Ex: C1 2 -> C1_2"
    print ""
# <<fold
def _writeMolFile(comments, molecule, dalton_mol_filename): # fold>>
    molfile = MolFile()
    
    molfile.addComment(comments[0], comments[1])
    molfile.setSymmetryGenerators(molecule.symmetry_generators)

    for label, element, symmetry, coordinates in zip(molecule.labels_list, molecule.elements_list, molecule.symmetries_list, molecule.coordinates_list) :
        if symmetry != "1" and symmetry != "":
            continue
        molfile.addAtom(label, element, coordinates, molecule.basis_set)
    
    outfile = file(dalton_mol_filename,"w")
    outfile.write(molfile.generateOutput())
    outfile.close()
# <<fold

def main(argv): # fold>>

    options = _getOptions(argv)

    parser = Parser(options.dalton_out_filename)
    molecule = parser.getMolecule()  

    if options.basis is not None:
        molecule.basis_set = options.basis

    if options.align is True:
        molecule = _alignMolecule(molecule, options.relabel_symbols)
        molecule.symmetry_generators = []

    comments=("Created with dalOut2dalIn script",os.path.basename(options.dalton_out_filename))
    _writeMolFile(comments, molecule, options.dalton_mol_filename)
    # <<fold



if __name__ == "__main__":
    main(sys.argv)
