#/usr/bin/env python
# @author Stefano Borini

import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
import traceback
import shutil
from lib import filestorage
from lib import uuid
from wavemoldb import ordfm
from wavemoldb.ordfm import contexts
from wavemoldb.ordfm import grrm2
from application import graphstore
import settings

import rdflib
from rdflib import store
from rdflib.Graph import Graph as ContextGraph

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

import logging
import getopt

class Options:
    def __init__(self, argv): 
        self.show = None
        self.quads = False
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "rnoca:lh", ["runs","molecules", "originalsubmissions", "contexts", "about=", "all", "help"])

        for opt in opts:
            if opt[0] in ["-r", "--runs"]:
                self.show= "runs"
            if opt[0] in ["-l", "--all"]:
                self.show= "all"
            if opt[0] in ["-m", "--molecules"]:
                self.show= "molecules"
            if opt[0] in ["-o", "--originalsubmissions"]:
                self.show= "originalsubmissions"
            if opt[0] in ["-c", "--contexts"]:
                self.show= "contexts"
            if opt[0] in ["-a", "--about"]:
                self.show= "about"
                self.about = opt[1]

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --option"
    print ""
    print "options are runs, molecules, originalsubmissions, about, contexts"
    print ""
    if error is not None:
        print ""
        print error
        print ""

base_graph = None

options = Options(sys.argv)
base_graph = graphstore.graph()
print "triples: "+str(len(base_graph))

if options.show == "runs":
    for r in ordfm.grrm2.Run.all(base_graph):
        print r.uri()
elif options.show == "molecules":
    for r in ordfm.grrm2.Molecule.all(base_graph):
        print r.uri()
elif options.show == "originalsubmissions":
    for r in ordfm.OriginalSubmission.all(base_graph):
        print r.uri()
elif options.show == "about":
    s = rdflib.URIRef(options.about)
    for p,o in base_graph.predicate_objects(s):
        print s.n3(), p.n3(), o.n3()
elif options.show == "all":
    for s,p,o,ctx in base_graph.quads( (None, None, None)):
        print s.n3(), p.n3(), o.n3(), ctx
elif options.show == "contexts":
    for ctx in set(base_graph.contexts()):
        print ctx
