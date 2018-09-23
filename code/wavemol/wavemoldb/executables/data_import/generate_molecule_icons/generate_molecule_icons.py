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
import time

JMOL_PATH = "../../../web/applets/jmol/jmol.sh"

if not os.path.exists(JMOL_PATH):
    print "Unable to find jmol"
    sys.exit(1)

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

class Options:
    def __init__(self, argv): 
        self.submission_uuid = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:vh", ["id=","verbose", "help"])

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
    print "Generate xyz for all molecules in a given submission"
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


for mol in grrm2.Molecule.all(graph):
    fs = filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)

    all_files=[]
    proc=[]

    fd, temp_path = tempfile.mkstemp()

    os.write(fd, "load "+fs.path("geometry", "xyz")+"\n")
    os.write(fd, "rotate x 0\n")
    os.close(fd)

    output_png = fs.path("icon", "png")
    all_files.append(output_png)
    print "creating image for molecule "+output_png
    proc.append(subprocess.Popen("export DISPLAY=:5; "+JMOL_PATH+" -g64x64 -ions "+temp_path+" -w PNG:"+output_png, shell=True))

    output_png = fs.path("icon", "png", parameters={"size": "256x256"})
    print "creating large image for molecule "+output_png
    proc.append(subprocess.Popen("export DISPLAY=:5; "+JMOL_PATH+" -g256x256 -ions "+temp_path+" -w PNG:"+output_png, shell=True))

    for angle in xrange(0, 360, 20):
        fd, temp_path = tempfile.mkstemp()

        os.write(fd, "load "+fs.path("geometry", "xyz")+"\n")
        os.write(fd, "rotate x "+str(angle)+"\n")
        os.close(fd)

        output_png = fs.path("icon", "png", parameters={"angle": angle})
        all_files.append(output_png)
        print "creating image for molecule "+output_png+" angle "+str(angle)
        proc.append(subprocess.Popen("export DISPLAY=:5; "+JMOL_PATH+" -g64x64 -ions "+temp_path+" -w PNG:"+output_png, shell=True))

    for p in proc:
        sts = os.waitpid(p.pid, 0)[1]

    print "creating animated gif"
    os.system("convert "+" ".join(all_files)+" "+fs.path("animatedicon", "gif"))

