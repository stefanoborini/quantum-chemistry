#!/usr/bin/env python
import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
import traceback
from lib import uuid
from wavemoldb import ordfm
from wavemoldb.ordfm import grrm2
from wavemoldb.ordfm import contexts
from lib import filestorage
import rdflib
from application import graphstore
import settings
from rdflib.Graph import Graph
from rdflib.Graph import ReadOnlyGraphAggregate
from lib import indexing
import md5
import getopt
import copy

def _get_system_uuid(store, submission_uuid):
    graph = Graph(store, identifier=contexts.CONTEXT_NS.SubmissionInfo)
    submission = ordfm.OriginalSubmission.get(graph,uri="urn:uuid:"+submission_uuid)
    if submission is None:
        raise Exception("no submission found "+str(submission_uuid))
    storage = filestorage.ResourceStorage(submission, web_accessible=False, settings=settings.filestorage_settings)
    f=file(storage.path("system","uuid"), "r")
    id = str(uuid.UUID(f.readlines()[0]))
    f.close()
    return id


class Options:
    def __init__(self, argv): 
        self.submission_uuid = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:vh", ["id=","help"])

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
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=submission_uuid"
    print ""
    print "Indicize the interesting values from the latest submission, to allow search"
    print ""
    if error is not None:
        print ""
        print error
        print ""

class Data(object):
    def __init__(self):
        self.is_grrm__molecule = False
        self.is_grrm__equilibrium_structure = False
        self.is_grrm__transition_state = False
        self.is_grrm__barrierless_dissociated = False
        self.is_grrm__barrier_dissociated = False
        self.is_grrm__interconversion_step = False
        self.is_grrm__interconversion = False
        self.is_grrm__run = False
        self.grrm__energy = None
        self.grrm__mass = None
        self.grrm__basis_set = None
        self.grrm__carbons = None
        self.grrm__oxygens = None
        self.grrm__hydrogens = None
        self.grrm__nitrogens = None
        self.grrm__smiles_md5 = None
        self.grrm__inchi_md5 = None
        self.grrm__canost_planar_md5 = None

    def __str__(self):
        return str([self.is_grrm__molecule,
        self.is_grrm__equilibrium_structure,
        self.is_grrm__transition_state,
        self.is_grrm__barrierless_dissociated,
        self.is_grrm__barrier_dissociated,
        self.is_grrm__interconversion_step,
        self.is_grrm__interconversion,
        self.is_grrm__run,
        self.grrm__energy,
        self.grrm__mass,
        self.grrm__basis_set,
        self.grrm__carbons,
        self.grrm__oxygens,
        self.grrm__hydrogens,
        self.grrm__nitrogens,
        self.grrm__smiles_md5,
        self.grrm__inchi_md5,
        self.grrm__canost_planar_md5])
    def toDict(self):
        d = {}
        d["is_grrm__molecule"]                = self.is_grrm__molecule                   
        d["is_grrm__equilibrium_structure"]   = self.is_grrm__equilibrium_structure 
        d["is_grrm__transition_state"]        = self.is_grrm__transition_state 
        d["is_grrm__barrierless_dissociated"] = self.is_grrm__barrierless_dissociated 
        d["is_grrm__barrier_dissociated"]     = self.is_grrm__barrier_dissociated 
        d["is_grrm__interconversion_step"]    = self.is_grrm__interconversion_step 
        d["is_grrm__interconversion"]         = self.is_grrm__interconversion 
        d["is_grrm__run"]                     = self.is_grrm__run 
        d["grrm__energy"]                     = self.grrm__energy 
        d["grrm__mass"]                       = self.grrm__mass
        d["grrm__basis_set"]                  = self.grrm__basis_set
        d["grrm__carbons"]                    = self.grrm__carbons 
        d["grrm__oxygens"]                    = self.grrm__oxygens 
        d["grrm__hydrogens"]                  = self.grrm__hydrogens 
        d["grrm__nitrogens"]                  = self.grrm__nitrogens 
        d["grrm__smiles_md5"]                 = self.grrm__smiles_md5 
        d["grrm__inchi_md5"]                  = self.grrm__inchi_md5 
        d["grrm__canost_planar_md5"]          = self.grrm__canost_planar_md5              
        return d

def grrmTypeFilter(thing, data_list):
    if grrm2.Molecule.tryCast(thing):
        for data in data_list:
            data.is_grrm__molecule = True

    if grrm2.EquilibriumStructure.tryCast(thing):
        for data in data_list:
            data.is_grrm__equilibrium_structure = True

    if grrm2.TransitionState.tryCast(thing):
        for data in data_list:
            data.is_grrm__transition_state = True

    if grrm2.BarrierlessDissociated.tryCast(thing):
        for data in data_list:
            data.is_grrm__barrierless_dissociated = True
       
    if grrm2.BarrierDissociated.tryCast(thing):
        for data in data_list:
            data.is_grrm__barrier_dissociated = True
    
    if grrm2.InterconversionStep.tryCast(thing):
        for data in data_list:
            data.is_grrm__interconversion_step = True
    
    if grrm2.Interconversion.tryCast(thing):
        for data in data_list:
            data.is_grrm__interconversion = True
    
    if grrm2.Run.tryCast(thing):
        for data in data_list:
            data.is_grrm__run = True


    return (thing, data_list)

def grrmMoleculeInfoFilter(thing, data_list):
    if not grrm2.Molecule.tryCast(thing):
        return (thing, data_list)

    mol = grrm2.Molecule.tryCast(thing)
    energy = grrm2.energy(mol).get()
    if energy:
        for data in data_list:
            data.grrm__energy = float(energy)

    mass = grrm2.mass(mol).get()
    if mass:
        for data in data_list:
            data.grrm__mass = float(mass)

    geometry = grrm2.geometry(mol).get()
    if geometry:
        for data in data_list:
            all_symbols = geometry["symbols"]
            data.grrm__carbons = len(filter(lambda x: x == "C", all_symbols))
            data.grrm__oxygens = len(filter(lambda x: x == "O", all_symbols))
            data.grrm__hydrogens = len(filter(lambda x: x == "H", all_symbols))
            data.grrm__nitrogens = len(filter(lambda x: x == "N", all_symbols))

    smiles = grrm2.smiles(mol).get()
    if smiles:
        for data in data_list:
            data.grrm__smiles_md5 = md5.md5(smiles).hexdigest()
    inchi = grrm2.inchi(mol).get()
    if inchi:
        for data in data_list:
            data.grrm__inchi_md5 = md5.md5(inchi).hexdigest()

    return (thing, data_list)

def grrmCanostFilter(thing, data_list):
    mol = grrm2.Molecule.tryCast(thing)
    if not mol:
        return (thing, data_list)

    canost_codes = grrm2.canostPlanar(mol).get()
    if not canost_codes:
        return (thing, data_list)

    new_data_list = []
    for code in canost_codes:
        print code
        for data in data_list:
            new_data = copy.deepcopy(data)
            new_data.grrm__canost_planar_md5 = md5.md5(code).hexdigest()
            new_data_list.append(new_data)
        
    return (thing, new_data_list)

def grrmBasisSetFilter(thing, data_list):
    run = grrm2.Run.tryCast(thing)
    runoutput = grrm2.RunOutput.tryCast(thing)
    
    if run:
        for inputs in grrm2.runInput(run).get():
            run_data = grrm2.RunData.tryCast(inputs[0])
            if run_data:
                for data in data_list:
                    data.grrm__basis_set = grrm2.basisSet(run_data).get()
    elif runoutput:
        try:
            run = grrm2.runOutputOf(runoutput).get()[0]
            if run:
                for inputs in grrm2.runInput(run).get():
                    run_data = grrm2.RunData.tryCast(inputs[0])
                    if run_data:
                        for data in data_list:
                            data.grrm__basis_set = grrm2.basisSet(run_data).get()
        except:
            pass
            
 
    return (thing, data_list)
def _getDataList(thing):
    return grrmBasisSetFilter( *grrmCanostFilter( *grrmTypeFilter( *grrmMoleculeInfoFilter(thing, [ Data() ]) ))) 


    

options=Options(sys.argv)

submission_graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+options.submission_uuid))
sys_uuid = _get_system_uuid(graphstore.store(), options.submission_uuid)
sys_graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+sys_uuid))
graph=ReadOnlyGraphAggregate([submission_graph, sys_graph])

try:
    indexer = indexing.DbIndex()
    indexer.addIndex("is_grrm__molecule", "BOOLEAN")
    indexer.addIndex("is_grrm__equilibrium_structure", "BOOLEAN")
    indexer.addIndex("is_grrm__transition_state", "BOOLEAN")
    indexer.addIndex("is_grrm__barrierless_dissociated", "BOOLEAN")
    indexer.addIndex("is_grrm__barrier_dissociated", "BOOLEAN")
    indexer.addIndex("is_grrm__interconversion_step", "BOOLEAN")
    indexer.addIndex("is_grrm__interconversion", "BOOLEAN")
    indexer.addIndex("is_grrm__run", "BOOLEAN")
    indexer.addIndex("grrm__energy", "FLOAT")
    indexer.addIndex("grrm__mass", "FLOAT")
    indexer.addIndex("grrm__basis_set", "VARCHAR(32)")
    indexer.addIndex("grrm__carbons", "INTEGER")
    indexer.addIndex("grrm__oxygens", "INTEGER")
    indexer.addIndex("grrm__hydrogens", "INTEGER")
    indexer.addIndex("grrm__nitrogens", "INTEGER")
    indexer.addIndex("grrm__smiles_md5", "VARCHAR(32)")
    indexer.addIndex("grrm__inchi_md5", "VARCHAR(32)")
    indexer.addIndex("grrm__canost_planar_md5", "VARCHAR(32)")

    for thing in grrm2.Thing.all(graph):
        indexer.delete(thing.uri())
        for data in _getDataList(thing)[1]:
            print thing.uri(), data
            indexer.store(thing.uri(), data.toDict())

except Exception, e:
    traceback.print_exception(*sys.exc_info()) 
    sys.exit(1)

sys.exit(0)


