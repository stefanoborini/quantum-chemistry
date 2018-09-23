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
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:h", ["id=", "help"])

        for opt in opts:
            if opt[0] in ["-i", "--id"]:
                self.submission_uuid = str(uuid.UUID(opt[1]))
            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)

        if self.submission_uuid is None:
            _usage()
            sys.exit(1)

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=uuid"
    print ""
    print "Creates or returns the existent system identifier for a given original submission identifier."
    print "The system identifier is a submission identifier for information computed by the system."
    print "This mechanism is in place to keep user-provided info from system-provided info. Also,"
    print "the concept behind the import queue is idempotency, so if a file with the system identifier"
    print "is found, it will be returned instead of being created anew (since it's random)"
    print ""
    if error is not None:
        print ""
        print error
        print ""

def _generate_id(submission):
    storage = filestorage.ResourceStorage(submission, web_accessible=False, settings=settings.filestorage_settings)
    f=file(storage.path("system","uuid"), "w")
    f.write(str(uuid.uuid4()))
    f.close()
    return _get_id(submission)

def _get_id(submission):
    storage = filestorage.ResourceStorage(submission, web_accessible=False, settings=settings.filestorage_settings)
    f=file(storage.path("system","uuid"), "r")
    id = str(uuid.UUID(f.readlines()[0]))
    f.close()
    return id


base_graph = None
submission_info_subgraph = None

try:
    options = Options(sys.argv)

    base_graph = graphstore.graph()
    submission_info_subgraph = ContextGraph(base_graph.store, identifier=contexts.CONTEXT_NS.SubmissionInfo)

    submission = ordfm.OriginalSubmission.get(submission_info_subgraph,uri="urn:uuid:"+options.submission_uuid)
    if submission is None:
        _usage("unexistent submission")
        sys.exit(1)

    try:
        id = _get_id(submission)
    except:
        id = _generate_id(submission)

    print id    

except Exception, e:
    traceback.print_exception(*sys.exc_info())
    sys.exit(1)

sys.exit(0)
