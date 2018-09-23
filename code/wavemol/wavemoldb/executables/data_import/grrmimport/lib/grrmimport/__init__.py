#/usr/bin/env python
# @author Stefano Borini
# @description this script extracts various data from a dalton file and imports it into a
# @description specified database.
# @description It uses TheoChemPy > 0.12.0
# @license Artistic License 2.0

import os
import sys
if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(1,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

import logging
from . import printout
from . import submitters
from . import grrmparser
import getopt
class Options:
    def __init__(self, argv): # fold>>
        self.db_url = None
        self.output = None
        self.grrm_dir = None
        self._getOptions(argv)
    # <<fold 
    def _getOptions(self,argv): # fold>>
        opts, args=getopt.getopt(argv[1:], "u:o:vh", ["db-url=", "output=", "verbose", "help"])

        for opt in opts:
            db_url = self._getOptionArg(opt, "-u","--db-url")
            if db_url:
                self.db_url = db_url

            output = self._getOptionArg(opt, "-o","--output")
            if output:
                self.output = output

            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)
            if opt[0] in [ "-v", "--verbose"]:
                logging.basicConfig(level=logging.DEBUG)
                
        try:
            self.grrm_dir = args[0]
        except:
            _usage("Required information missing : grrm output directory")
            sys.exit(1)

        if self.db_url is None and self.output is None:
            _usage("Required information missing : target file/database url")
            sys.exit(1)
            
        # <<fold
    def _getOptionArg(self, opt, short, long, not_empty=True):
        if opt[0] in [short, long]:
            if len(opt[1].strip()) == 0 and not_empty:
                _usage("Empty value in "+short+"/"+long)
                sys.exit(1)
            return opt[1].strip()
        return None
       

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" [options] grrm_run_directory"
    print ""
    print "--verbose"
    print "                Be verbose (for debug)"
    print "--db-url=URL"
    print "                The base URL database to use for import."
    print "--output=file.xml"
    print "                Writes the final RDF representation to file.xml"
    print ""
    print ""
    if error is not None:
        print ""
        printout.error(error)
        print ""

def main():
    argv = sys.argv
    options = Options(argv)
    printout.keyvalue("grrm_dir",str(options.grrm_dir))

    sub = []

    if options.db_url:
        sub.append( submitters.HttpSubmitter(options.db_url) )

    if options.output:
        sub.append( submitters.FileSubmitter(options.output) )
        
    graph = grrmparser.GRRMParser().parse(options.grrm_dir)

    rdfxml = graph.serialize()
    for s in sub:     
        s.submit(rdfxml)
