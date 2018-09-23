#/usr/bin/env python
# @author Stefano Borini
# @description this script converts a zmat file into a dalton mol file.
# @description It uses TheoChemPy.
# @license Artistic License 2.0

import os
import sys
import getopt

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(1,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

from theochempy._theochempy.FileParsers import ZMatrix
from theochempy._theochempy.InputGenerators import Dalton20
from theochempy._theochempy.Chemistry import PeriodicTable
from theochempy._theochempy import Measure
from theochempy._theochempy import Units
from theochempy._theochempy import Math


class Options:
    def __init__(self): # fold>>
        self.translate = None
        self.input_filename = None
        self.output_filename = None
    # <<fold

def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "t:h", ["translate=", "help"])

    for opt in opts:
        if opt[0] == "-t" or opt[0] == "--translate":
            try:
                print opt[1]
                t = tuple(map(float, opt[1].split(",")))
            except:
                _usage("unable to convert translation vector")
                sys.exit(1)

            if len(t) != 3:
                _usage("translation vector length is not equal to 3")
                sys.exit(1)
                
            options.translate = Measure.Measure(t, Units.angstrom)
            
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)
    
    if len(args) < 2:
        _usage("Too few arguments")
        sys.exit(1)

    options.input_filename = args[0]
    options.output_filename = args[1]

    return options
    # <<fold

def _usage(error=None): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" [--translate=x,y,z] filename_in filename_out"
    print ""
    print "--translate=x,y,z"
    print "                translate the molecule of a given amount before writing the output file"
    print ""
    if error is not None:
        print ""
        print "Error : "+error
        print ""
# <<fold

def writeDalton20(zmatrix_parser, filename, translate): # fold>>
    """
    this routine prints the dalton .mol format for the given molecule
    in dalton 2.0 format
    """
    cartcoord = zmatrix_parser.cartesianCoords()
    
    molfile = Dalton20.MolFile()
    
    molfile.setSymmetryGenerators(zmatrix_parser.symmetries())

    atom_counter = {}
    for entry in cartcoord:
        symbol = entry[0]
        if symbol == PeriodicTable.Dummy.symbol():
            continue 

        coords = Measure.Measure(entry[1].value(), zmatrix_parser.distanceUnits())
        if translate is not None:
            coords = coords + translate
            coords = Measure.Measure(Math.Vector3(*coords.value()), zmatrix_parser.distanceUnits())

        basis = entry[2]
        if atom_counter.has_key(symbol):
            atom_counter[symbol] += 1
        else:
            atom_counter[symbol] = 1
        molfile.addAtom(symbol+str(atom_counter[symbol]), PeriodicTable.getElementBySymbol(symbol), coords, basis)
        
    # ok... now produce the .mol input...
    
    f=file(filename,"w")
    f.write(molfile.generateOutput())
    f.close()
# <<fold 

def main(argv): # fold>>
    
    options = _getOptions(argv)

    a=ZMatrix.ZMatrixParser()
    a.parseFile(options.input_filename)
    writeDalton20(a,options.output_filename, options.translate)


if __name__ == '__main__':
    main(sys.argv)



