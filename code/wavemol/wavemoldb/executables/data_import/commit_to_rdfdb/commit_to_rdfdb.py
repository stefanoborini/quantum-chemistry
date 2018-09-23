#/usr/bin/env python
# @author Stefano Borini

import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
import traceback
import shutil
from lib import filestorage
from lib import uuid
from wavemoldb import ordfm
from wavemoldb.ordfm import namespaces
from wavemoldb.ordfm import contexts
from application import graphstore
import settings

import rdflib
from rdflib import store
from rdflib.Graph import Graph as ContextGraph

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

import getopt

class Options:
    def __init__(self, argv): 
        self.submission_uuid = None
        self.submission_file = None
        self.system_uuid = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:s:h", ["id=", "sys-id=", "help"])

        for opt in opts:
            if opt[0] in ["-i", "--id"]:
                self.submission_uuid = str(uuid.UUID(opt[1]))
            if opt[0] in ["-s", "--sys-id"]:
                self.system_uuid = str(uuid.UUID(opt[1]))
            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)

        fs = filestorage.FileStorage("importer", web_accessible=False, settings=settings.filestorage_settings)
        self.submission_file = fs.path(self.submission_uuid+".rdf")

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=uuid --sys-id=uuid"
    print ""
    print "Submit to the triplestore the rdf file for a given submission uuid."
    print ""
    if error is not None:
        print ""
        print error
        print ""

base_graph = None
submission_info_subgraph = None

try:
    options = Options(sys.argv)
    base_graph = graphstore.graph()
    submission_info_subgraph = ContextGraph(base_graph.store, identifier=contexts.CONTEXT_NS.SubmissionInfo)

    submission = ordfm.OriginalSubmission.get(submission_info_subgraph,uri="urn:uuid:"+options.submission_uuid)
    if submission is None:
        submission = ordfm.OriginalSubmission.new(submission_info_subgraph,uri="urn:uuid:"+options.submission_uuid)
    else:
        print "Previous submission found. overwriting"
        base_graph.remove_context(rdflib.URIRef("urn:uuid:"+options.submission_uuid))

    storage = filestorage.ResourceStorage(submission, web_accessible=False, settings=settings.filestorage_settings)
    if storage.readable("submission","rdf"):
        print "file already present. overwriting"
    
    shutil.copyfile(options.submission_file, storage.path("submission","rdf"))

    submission_subgraph = ContextGraph(base_graph.store, identifier=rdflib.URIRef("urn:uuid:"+options.submission_uuid))
    submission_subgraph.parse(storage.path("submission","rdf"))

    print "committing"
    submission_subgraph.commit()
    submission_info_subgraph.commit()
    print "done"
    print "new triple count : "+str(len(base_graph))

except Exception, e:
    if base_graph:
        base_graph.rollback()
    if submission_info_subgraph:
        submission_info_subgraph.rollback()
    traceback.print_exception(*sys.exc_info())
    sys.exit(1)

sys.exit(0)
