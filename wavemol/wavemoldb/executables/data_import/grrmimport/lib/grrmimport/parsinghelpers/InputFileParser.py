from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes

from wavemoldb.ordfm import grrm2

from .. import uuid
import rdflib
from . import helperfuncs

class InputFileParser:
    def __init__(self, graph, filename):
        self._graph = graph
        self._filename = filename
        self._run = None
        self._molecule = None
        self._parseInput() 

    def run(self):
        return self._run
    def molecule(): 
        return self._molecule_uri

    def _parseInput(self):
        input_tokenizer = grrm.InputTokenizer()
        token_list = input_tokenizer.tokenize(self._filename)

        molecule_dict = {}
        run_dict = {}
        for t in token_list:
            if t.__class__ == tokentypes.InputGeometryToken:
                molecule_dict["charge"] = int(t.charge())
                molecule_dict["spin_multiplicity"] = int(t.spinMultiplicity())
                molecule_dict["geometry"] = helperfuncs.parseGeometryToken(t)
            elif t.__class__ == tokentypes.CommandDirectiveToken:
                run_dict["job"] = t.jobString() 
                run_dict["method"] = t.methodString()
                run_dict["basis_set"] = t.basisSetString()

        molecule = grrm2.Molecule.new(self._graph,rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        grrm2.geometry(molecule).set(molecule_dict["geometry"]) 
        grrm2.spinMultiplicity(molecule).set(molecule_dict["spin_multiplicity"])
        grrm2.charge(molecule).set(molecule_dict["charge"])

        rundata = grrm2.RunData.new(self._graph, rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        grrm2.job(rundata).set(run_dict["job"])
        grrm2.method(rundata).set(run_dict["method"])
        grrm2.basisSet(rundata).set(run_dict["basis_set"])

        run = grrm2.Run.new(self._graph, rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        grrm2.runInput(run).add(rundata)
        grrm2.runInput(run).add(molecule)

        self._run = run
        self._molecule = molecule

