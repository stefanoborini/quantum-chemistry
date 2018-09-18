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

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=submission_uuid"
    print ""
    print "Generate xyz for all molecules in a given submission"
    print ""
    if error is not None:
        print ""
        print error
        print ""

options=Options(sys.argv)

graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+str(options.submission_uuid)))

for mol in grrm2.Molecule.all(graph):
    fs = filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)

    data = grrm2.geometry(mol).get()
    elements = data["symbols"]
    coords = data["coordinates"]

    f = file(fs.path("geometry","xyz"), "w")

    num_atoms = len(elements)
    f.write(str(num_atoms)+"\n\n")
    for element, coord in zip(elements, coords):
        f.write( "%s  %16.10f %16.10f %16.10f\n" % (element, coord[0], coord[1], coord[2]) )

    f.close()

    fragments = grrm2.fragments(mol).get()
    if fragments:
        for fragment_number, fragment in enumerate(fragments):
            print mol.uri()
            f = file(fs.path("geometry","xyz", parameters={"fragment" : fragment_number}), "w")
            f.write(str(len(fragment))+"\n\n")
            for index in fragment:
                f.write("%s  %16.10f %16.10f %16.10f\n" % (elements[index-1], coords[index-1][0], coords[index-1][1], coords[index-1][2]))
            f.close()


            
