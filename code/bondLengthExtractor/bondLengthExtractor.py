#/usr/bin/env python

# @description this script extracts all the carbon carbon distance from a dalton output file
# @description It uses TheoChemPy.

from TheoChemPy.FileParsers import Dalton
from TheoChemPy.FileParsers.Dalton import Tokens

import sys

def main(filename):
    tokens = Dalton.tokenizeOutFile(filename)

    try:
        bond_length_token = filter(lambda x: x.__class__ == Tokens.BondLengthsToken, tokens)[-1]
    except:
        print "Sorry, looks like there are no bond length entries in the file"
        sys.exit(1)

    atom_list = bond_length_token.atomList()

    print "# %s" % (filename, )
    for entry in atom_list:
        if entry[0][0][0] == "C" and entry[1][0][0] == "C":
            print "%s %s %s %s %s" % (entry[0][0], entry[0][1], entry[1][0], entry[1][1], entry[2])

        


def getDistance(token, label1, sym1, label2, sym2):
    for entry in token.atomList():
        if entry[0][0] == label1 and entry[0][1] == sym1 and entry[1][0] == label2 and entry[1][1] == sym2:
            return float(entry[2])

    return None



if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except:
        print "Usage : extractor.py filename"
        sys.exit(1)

    main(filename)
