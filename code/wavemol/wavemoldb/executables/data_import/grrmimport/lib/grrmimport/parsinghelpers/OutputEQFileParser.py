from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes
from wavemol.core import units
from wavemoldb.ordfm import grrm2

from . import helperfuncs
from .. import uuid
import rdflib

class OutputEQFileParser:
    def __init__(self, graph, filename):
        self._graph = graph
        self._filename = filename
        self._struct_label_to_molecule_mapper = {}
        self._molecules = []

        self._parseEQTokenList()

    def molecules(self):
        return self._molecules
    def structureLabelToMoleculeMapper(self):
        return self._struct_label_to_molecule_mapper
         
    def _parseEQTokenList(self): 
        current_molecule = None

        tokenizer = grrm.ListOutputTokenizer()
        tokens = tokenizer.tokenize(self._filename)

        header_found = False
        for t in tokens:
            if t.__class__ == tokentypes.HeaderEquilibriumToken:
                header_found = True
            if t.__class__ == tokentypes.StructureHeaderToken:
                if not header_found:
                    raise Exception("Header not found")
                current_molecule = grrm2.EquilibriumStructure.new(self._graph,rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
                self._molecules.append(current_molecule)
                grrm2.structureNumber(current_molecule).set(int(t.number()))

                self._struct_label_to_molecule_mapper[ ("EQ", t.number()) ] = current_molecule

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


