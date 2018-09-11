#/usr/bin/env python
# @author Stefano Borini
# @description performs linear regression on a given dataset
# @license Artistic License 2.0

import os
import sys
import getopt

from theochempy._theochempy.IO import XYZFile
from theochempy._theochempy.Molecules import XYZMolecule

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

import numpy
from scipy import stats


class Options:
    def __init__(self): # fold>>
        self.input_filename = None
        self.output_filename = None
    # <<fold

def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "h", ["help"])

    for opt in opts:
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)

    if len(args) == 2:
        options.input_filename = args[0]
        options.output_filename = args[1]

    return options
    # <<fold

def _usage(): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" input output"
    print ""
    print "Accepts a xyz file containing one or more molecules. Center each molecule into its center of mass."
    print ""
# <<fold

def main(argv): # fold>>

    options = _getOptions(argv)

    infile = XYZFile.XYZFile(options.input_filename)
    outfile = XYZFile.XYZFile()


    for mol_idx in xrange(infile.numOfMolecules()):
        atom_list = []
        for atom_idx in xrange(infile.numOfAtoms(mol_idx)):
            atom_list.append(infile.atom(mol_idx, atom_idx))
            

        molecule = XYZMolecule.XYZMolecule(atom_list)
        molecule.translate(-XYZMolecule.centerOfMass(molecule))

        new_mol_index = outfile.createMolecule()
        for atom in zip(molecule.elements(), molecule.atomPos()):
            outfile.addAtom(new_mol_index,atom)
            


    outfile.saveTo(options.output_filename)
    # <<fold


if __name__ == "__main__":
    main(sys.argv)



