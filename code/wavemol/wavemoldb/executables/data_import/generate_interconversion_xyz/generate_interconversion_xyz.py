#!/usr/bin/env python
import subprocess
import tempfile
import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
from lib import filestorage
from lib import uuid
from wavemoldb import ordfm
from application import graphstore
import settings
import rdflib
from wavemoldb.ordfm import grrm2
from rdflib.Graph import Graph
import getopt

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

class Options:
    def __init__(self, argv): 
        self.submission_uuid = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:vh", ["id=", "verbose", "help"])

        for opt in opts:
            if opt[0] in ["-i", "--id"]:
                self.submission_uuid = str(uuid.UUID(opt[1]))
            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)
            if opt[0] in [ "-v", "--verbose"]:
                logging.basicConfig(level=logging.DEBUG)

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=submission_uuid"
    print ""
    print "Generate xyz for the interconversions in a given submission"
    print ""
    if error is not None:
        print ""
        print error
        print ""

options=Options(sys.argv)
if options.submission_uuid is None:
    _usage()
    sys.exit(1)

graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+str(options.submission_uuid)))

for iconv in grrm2.Interconversion.all(graph):
    print "Generating xyz for interconversion "+iconv.uri()
    res_storage=filestorage.ResourceStorage(iconv, web_accessible=True, settings=settings.filestorage_settings)

    all_files = []

    step_tuples = []
    for s in grrm2.interconversionStep(iconv).getAll():
        step = s[0] 
        fs= filestorage.ResourceStorage(step, web_accessible=True, settings=settings.filestorage_settings)
        step_xyz = fs.path("geometry","xyz")
        step_number = grrm2.stepNumber(step).get()
        step_tuples.append( (step_number, step_xyz))

    def cmpFunc(x,y):
        return cmp(x[0], y[0]) 
    for step, file in sorted(step_tuples, cmp=cmpFunc):
        all_files.append(file)

    if len(all_files) != 0:
        os.system("cat "+" ".join(all_files+list(reversed(all_files)))+" >"+res_storage.path("geometry", "xyz"))

