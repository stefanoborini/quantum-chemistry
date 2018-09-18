#!/usr/bin/env python
import subprocess
import tempfile
import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
from lib import filestorage
from lib import uuid
from wavemoldb import ordfm
from wavemoldb.ordfm import grrm2
import rdflib
from application import graphstore
import settings
from lib import chemistry
from lib import utils
from rdflib.Graph import Graph
import getopt

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

class Options:
    def __init__(self, argv): 
        self.submission_uuid = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:h", ["id=","help"])

        for opt in opts:
            if opt[0] in ["-i", "--id"]:
                self.submission_uuid = str(uuid.UUID(opt[1]))
            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)
        if self.submission_uuid is None:
            _usage("Missing --id parameter")
            sys.exit(1)
def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=submission_uuid"
    print ""
    print "Generate interconversion network files"
    print ""
    if error is not None:
        print ""
        print error
        print ""

def _getLabel(mol):
    struct_number = grrm2.structureNumber(mol).get()
    if grrm2.EquilibriumStructure.tryCast(mol):
        struct_type = "EQ"
    elif grrm2.TransitionState.tryCast(mol):
        struct_type = "TS"
    elif grrm2.BarrierlessDissociated.tryCast(mol):
        struct_type = "uDC"
    elif grrm2.BarrierDissociated.tryCast(mol):
        struct_type = "dDC"

    return struct_type+str(struct_number)

options=Options(sys.argv)
graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+str(options.submission_uuid)))

runs = list(grrm2.Run.all(graph))

if len(runs) != 1:
    raise Exception("Run length != 1")

storage = filestorage.ResourceStorage(runs[0], web_accessible=True, settings=settings.filestorage_settings)
print "writing file : "+storage.path("connectivity","csv")
f=file(storage.path("connectivity","csv"),"w")
for icresult in grrm2.InterconversionResult.all(graph):
    label=_getLabel(icresult)
    f.write("v,"+label+","+utils.uriToUuid(icresult.uri())+"\n")


for iconv in grrm2.Interconversion.all(graph):
    start = grrm2.interconversionStart(iconv).get()[0]
    if grrm2.interconversionStart(iconv).get() is not None:
        start = grrm2.interconversionStart(iconv).get()[0]
    else:
        continue

    if grrm2.interconversionEnd(iconv).get() is not None:
        end = grrm2.interconversionEnd(iconv).get()[0]
    else:
        continue

    start_energy = grrm2.energy(start).get()
    end_energy = grrm2.energy(end).get()

    f.write("e,"+str(end_energy-start_energy)+","+_getLabel(start)+","+_getLabel(end)+","+utils.uriToUuid(iconv.uri())+"\n")

f.close()
