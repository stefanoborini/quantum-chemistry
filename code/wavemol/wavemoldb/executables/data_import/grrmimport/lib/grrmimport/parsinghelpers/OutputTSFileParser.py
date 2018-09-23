from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes
from wavemol.core import units
from wavemoldb.ordfm import grrm2

from .. import uuid
from . import helperfuncs
import rdflib

class OutputTSFileParser:
    def __init__(self, graph, filename):
        self._graph = graph
        self._filename = filename
        self._molecules = []
        self._struct_label_to_molecule_mapper = {}
        self._connections = []

        self._parseTSTokenList()
    def molecules(self):
        return self._molecules
    def structureLabelToMoleculeMapper(self):
        return self._struct_label_to_molecule_mapper
    def connections(self):
        return self._connections
    def _parseTSTokenList(self): # fold>>
        print "Parsing TS list file"
        tokenizer = grrm.ListOutputTokenizer()
        tokens = tokenizer.tokenize(self._filename)

        current_molecule = None

        header_found = False
        for t in tokens:
            if t.__class__ == tokentypes.HeaderTransitionToken:
                header_found = True
            if t.__class__ == tokentypes.StructureHeaderToken:
                if not header_found:
                    raise Exception("Header not found")
                id = "urn:uuid:"+str(uuid.uuid4())
                current_molecule = grrm2.TransitionState.new(self._graph,rdflib.URIRef(id))
                print "found TS "+str(t.number())+" : "+ str(id)
                grrm2.structureNumber(current_molecule).set(int(t.number()))

                self._molecules.append(current_molecule)
                self._struct_label_to_molecule_mapper[ ("TS", t.number())] = current_molecule

            if t.__class__ == tokentypes.GeometryToken:
                if not header_found:
                    raise Exception("Header not found")
                grrm2.geometry(current_molecule).set(helperfuncs.parseGeometryToken(t))
            if t.__class__ == tokentypes.EnergyToken:
                if not header_found:
                    raise Exception("Header not found")
                grrm2.energy(current_molecule).set(helperfuncs.parseEnergyToken(t))
            if t.__class__ == tokentypes.SpinToken:
                if not header_found:
                    raise Exception("Header not found")
                grrm2.spin(current_molecule).set(int(t.spin().rescale(units.hbar).magnitude))
            if t.__class__ == tokentypes.ZPVEToken:
                if not header_found:
                    raise Exception("Header not found")
                grrm2.zeroPointVibrationalEnergy(current_molecule).set(helperfuncs.parseZPVEToken(t))
            if t.__class__ == tokentypes.NormalModesToken:
                if not header_found:
                    raise Exception("Header not found")
                grrm2.normalModesEigenvalues(current_molecule).set(helperfuncs.parseNormalModesEigenvalues(t))
            if t.__class__ == tokentypes.ConnectionToken:
                if not header_found:
                    raise Exception("Header not found")
                print "Found connections "+str(t.first())+", "+str(t.second())

                if t.first() != "??":
                    type, number = t.first()[0:2], int(t.first()[2:])
                    if type == "DC":
                        type = "dDC"
                    self._connections.append( ( ( "TS", grrm2.structureNumber(current_molecule).get()), (type, number) ) )

                if t.second() != "??":
                    type, number = t.second()[0:2], int(t.second()[2:])
                    if type == "DC":
                        type = "dDC"
                    self._connections.append( ( ( "TS", grrm2.structureNumber(current_molecule).get()), (type, number) ) )



