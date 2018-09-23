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
        self.context = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "c:h", ["context=", "help"])

        for opt in opts:
            if opt[0] in ["-c", "--context"]:
                self.context = opt[1]

        if self.context is None:
            _usage()
            sys.exit(1)
def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --context=context_uuid"
    print ""
    if error is not None:
        print ""
        print error
        print ""

base_graph = None

options = Options(sys.argv)
base_graph = graphstore.graph()
print "triples: "+str(len(base_graph))

base_graph.remove_context(rdflib.URIRef("urn:uuid:"+str(uuid.UUID(options.context))))
base_graph.commit()

print "triples: "+str(len(base_graph))
