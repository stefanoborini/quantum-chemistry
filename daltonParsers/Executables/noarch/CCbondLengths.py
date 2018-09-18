#/usr/bin/env python
# @author Stefano Borini
# @description this script extracts all the carbon carbon distance from a dalton output file
# @description It uses TheoChemPy.
# @license Artistic License 2.0

import os
import sys

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens
from theochempy._theochempy import Units

def main(filename):
    tokens = Dalton20.tokenizeOutFile(filename)

    try:
        bond_length_token = filter(lambda x: x.__class__ == Tokens.BondLengthsToken, tokens)[-1]
    except:
        print "Sorry, looks like there are no bond length entries in the file"
        sys.exit(1)

    atom_list = bond_length_token.atomList()

    print "# %s" % (filename, )
    for entry in atom_list:
        if entry[0][0][0] == "C" and entry[1][0][0] == "C":
            print "%s %s %s %s %s" % (entry[0][0], entry[0][1], entry[1][0], entry[1][1], entry[2].asUnit(Units.angstrom).value())

        
if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage : "+os.path.basename(sys.argv[0])+" filename"
        sys.exit(1)

    main(filename)

