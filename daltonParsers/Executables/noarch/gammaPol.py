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
    print "Extracts the information about gamma polarizabilities from a Dalton file"
    print "The values are not in particular order. Each line contains the following setup"
    print ""
    print "bfreq|cfreq|dfreq|components|value|equal to"
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
    tokens = filter(lambda x: x.__class__ == Tokens.SecondHyperpolarizabilityToken, token_list)
    if len(tokens) == 0:
        raise Exception("Sorry. Could not find gamma component tokens")

    print "# bfreq|cfreq|dfreq|components|value|equal to"
    for t in tokens:
        printToken(t)


def formatComponents(components):
    i,j,k,l = components
    return i+";"+j+","+k+","+l

def printToken(t):
    for a in ("X", "Y", "Z"):
        for b in ("X", "Y", "Z"):
            for c in ("X", "Y", "Z"):
                for d in ("X", "Y", "Z"):
                    if t.gamma(a,b,c,d) is not None:
                        print "%7.6f|%7.6f|%7.6f|%s|%.8f|" % (t.BFreq().value(), t.CFreq().value(), t.DFreq().value(), formatComponents( (a,b,c,d) ),t.gamma(a,b,c,d).value())



if __name__ == "__main__":
    main(sys.argv)
