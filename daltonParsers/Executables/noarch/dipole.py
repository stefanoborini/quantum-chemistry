#/usr/bin/env python
# @author Stefano Borini
# @description this script extracts the gamma values from a dalton final file
# @description It uses TheoChemPy.
# @license Artistic License 2.0

import os
import sys

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens

def _usage():
    print "Usage: "+sys.argv[0]+" filename.out"
    print ""
    print "Extracts the information about the dipole from a Dalton file"
    print ""
    print "The dipole is returned as a single number. Unit is Debye"
    print "This is a basic copy of the values in dalton"

def main(argv): 

    if len(argv) < 2:
        _usage()
        sys.exit(1)

    dalton_out_filename = argv[1] 

    token_list = Dalton20.tokenizeOutFile(dalton_out_filename)
    tokens = filter(lambda x: x.__class__ == Tokens.DipoleMomentToken, token_list)
    if len(tokens) == 0:
        raise Exception("Sorry. Could not find dipole token")

    # take the last one, at the end of a geometry optimization, we have two of them
    print tokens[-1].dipole().value()


if __name__ == "__main__":
    main(sys.argv)
