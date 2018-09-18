#/usr/bin/env python
# @author Stefano Borini
# @description this script extracts the beta values from a dalton final file
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
    print "Extracts the information about beta polarizabilities from a Dalton file"
    print "The values are not in particular order. Each line contains the following setup"
    print ""
    print "bfreq|cfreq|components|value|equal to"
    print ""
    print "value can be empty, in the case a referenced value is pointed."
    print "please note that no guarantee is made on uniqueness of each entry."
    print "This is a basic copy of the values in dalton"

def main(argv): 

    if len(argv) < 2:
        _usage()
        sys.exit(1)

    dalton_out_filename = argv[1] 

    token_list = Dalton20.tokenizeOutFile(dalton_out_filename)
    tokens = filter(lambda x: x.__class__ == Tokens.FirstHyperpolarizabilityComponentToken, token_list)
    if len(tokens) == 0:
        raise Exception("Sorry. Could not find beta component tokens")

    print "# bfreq|cfreq|components|value|equal to"
    for t in tokens:
        if t.beta() is not None:
            print "%7.6f|%7.6f|%s|%.8f|" % (t.BFreq().value(), t.CFreq().value(), formatComponents(t.components()),t.beta().value())
        else:
            print "%7.6f|%7.6f|%s||%s" % (t.BFreq().value(), t.CFreq().value(), formatComponents(t.components()), formatComponents(t.refersTo())) 


def formatComponents(components):
    i,j,k = components
    return i+";"+j+","+k
if __name__ == "__main__":
    main(sys.argv)
