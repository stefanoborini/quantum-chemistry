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

import getopt


class Options:
    def __init__(self): # fold>>
        self.verbose = None
    # <<fold

def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "vh", ["verbose", "help"])

    for opt in opts:
        if opt[0] == "-a" or opt[0] == "--verbose":
            options.verbose=True
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)

    if len(args) != 1:
        _usage()
        sys.exit(1)

    if options.verbose is None:
        options.verbose = False

    options.dalton_out_filename = args[0]
    return options
    # <<fold

def _usage(): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" --verbose dalton_out_filename"
    print ""
    print "Check if the dalton file contains error. Returns 1 if errors. 0 if no errors."
    print "No message is returned on standard out or standard error."
    print ""
    print "--verbose : also prints out details about the found errors."
# <<fold

def _getErrorTokens(token_list): # fold>>
    tokens = filter(lambda x: x.__class__ == Tokens.SevereErrorToken, token_list)
    return tokens
    # <<fold

def main(argv): # fold>>

    options = _getOptions(argv)
    token_list = Dalton20.tokenizeOutFile(options.dalton_out_filename)

    error_tokens = _getErrorTokens(token_list)

    if options.verbose:
        for token in error_tokens:
            print "Error: "+token.reason()

    if len(error_tokens) != 0:
        sys.exit(1)

    sys.exit(0)

    # <<fold

if __name__ == "__main__":
    main(sys.argv)
