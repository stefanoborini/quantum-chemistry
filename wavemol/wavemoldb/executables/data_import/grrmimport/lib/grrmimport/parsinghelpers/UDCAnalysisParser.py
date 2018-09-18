from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes
from wavemol.core import units
from wavemoldb.ordfm import grrm2

from .. import uuid
from . import helperfuncs
from . import InterconversionAdditionalInfo
import rdflib
import re

class UDCAnalysisParser:
    def __init__(self, graph, filename):
        self._graph = graph
        self._filename = filename
        self._route = None
        self._route_steps = []
        self._route_additional_infos = None

        self._parseUDCAnalysis()

    def interconversions(self):
        return [ self._route ] 
    
    def interconversionSteps(self):
        return [ self._route_steps ]

    def interconversionAdditionalInfos(self):
        return [ self._route_additional_infos ] 

    def _parseUDCAnalysis(self):
        tokenizer = grrm.UDCAnalysisOutputTokenizer()
        tokens = tokenizer.tokenize(self._filename)
        
        steepest_header_found = False
        m_uDC = re.search("_uDC(\d+)\.log", self._filename)

        route = grrm2.Interconversion.new(self._graph, rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        self._route = route
        self._route_additional_infos = InterconversionAdditionalInfo.InterconversionAdditionalInfo(route)
        self._route_additional_infos.setStartStructureLabel( ( "uDC", int(m_uDC.group(1))) )

        steps = {}
        for t in tokens:
            if t.__class__ == tokentypes.SteepestDescentHeaderToken:
                steepest_header_found = True
            if t.__class__ == tokentypes.IRCStepToken:
                if not steepest_header_found:
                    raise Exception("Steepest Header not found")

                molecule = grrm2.InterconversionStep.new(self._graph, rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
                self._route_steps.append(molecule)
                grrm2.energy(molecule).set(t.energy().rescale(units.hartree).magnitude)
                grrm2.spin(molecule).set(t.spin().rescale(units.hbar).magnitude)
                grrm2.geometry(molecule).set(helperfuncs.parseGeometryToken(t))
                grrm2.stepNumber(molecule).set(t.step())

                grrm2.interconversionStep(route).add(molecule)
                steps[t.step()] = molecule
                if t.step() != 1:
                    grrm2.prevInterconversionStep(molecule).set(steps[t.step()-1]) 

            if t.__class__ == tokentypes.DownhillWalkingResultToken:
                self._route_additional_infos.setEndStructureLabel( t.result())

