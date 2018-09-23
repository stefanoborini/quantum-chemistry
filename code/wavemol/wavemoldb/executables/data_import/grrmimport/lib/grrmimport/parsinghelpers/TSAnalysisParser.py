from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes
from wavemol.core import units
from wavemoldb.ordfm import grrm2

from .. import uuid
from . import helperfuncs
from . import InterconversionAdditionalInfo
import rdflib
import re

class Anon: pass

class TSAnalysisParser:
    def __init__(self,graph, filename):
        self._graph = graph
        self._filename = filename
        self._forward_route = None
        self._backward_route = None
        self._forward_steps = []
        self._backward_steps = []
        self._forward_route_additional_infos = None
        self._backward_route_additional_infos = None

        self._parseTSAnalysis()

    def interconversions(self):
        return [self._forward_route, self._backward_route]

    def interconversionSteps(self):
        return [ self._forward_steps, self._backward_steps]

    def interconversionAdditionalInfos(self):
        return [ self._forward_route_additional_infos, self._backward_route_additional_infos ]

    def _parseTSAnalysis(self):
        tokenizer = grrm.TSAnalysisOutputTokenizer()
        tokens = tokenizer.tokenize(self._filename)

        status = Anon()
        status.header_found = False
        status.doing_forward = False
        status.doing_backward = False

        m_TS = re.search("_TS(\d+)\.log", self._filename)

        forward_route = grrm2.Interconversion.new(self._graph,rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        backward_route = grrm2.Interconversion.new(self._graph,rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        self._forward_route = forward_route
        self._backward_route = backward_route

        forward_steps = {}
        backward_steps = {}

        self._forward_route_additional_infos = InterconversionAdditionalInfo.InterconversionAdditionalInfo(forward_route)
        self._forward_route_additional_infos.setStartStructureLabel( ( "TS", int(m_TS.group(1)) ) )

        self._backward_route_additional_infos = InterconversionAdditionalInfo.InterconversionAdditionalInfo(backward_route)
        self._backward_route_additional_infos.setStartStructureLabel( ( "TS", int(m_TS.group(1)) ) )

        for t in tokens:
            if t.__class__ == tokentypes.IRCHeaderToken:
                status.header_found = True
            if t.__class__ == tokentypes.ForwardIRCHeaderToken:
                if not status.header_found:
                    raise Exception("Header not found")
                status.doing_forward = True
                status.doing_backward = False

            if t.__class__ == tokentypes.BackwardIRCHeaderToken:
                if not status.header_found:
                    raise Exception("Header not found")
                status.doing_forward = False
                status.doing_backward = True

            if t.__class__ == tokentypes.IRCStepToken:
                molecule = grrm2.InterconversionStep.new(self._graph, rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
                grrm2.energy(molecule).set(t.energy().rescale(units.hartree).magnitude)
                grrm2.spin(molecule).set(t.spin().rescale(units.hbar).magnitude)
                grrm2.geometry(molecule).set(helperfuncs.parseGeometryToken(t))
                grrm2.stepNumber(molecule).set(t.step())

                if status.doing_forward:
                    grrm2.interconversionStep(forward_route).add(molecule)
                    self._forward_steps.append(molecule)
                    forward_steps[t.step()] = molecule
                    if t.step() != 1:
                        grrm2.prevInterconversionStep(molecule).set(forward_steps[t.step()-1]) 
                     
                elif status.doing_backward:
                    grrm2.interconversionStep(backward_route).add(molecule)
                    self._backward_steps.append(molecule)

                    backward_steps[t.step()] = molecule
                    if t.step() != 1:
                        grrm2.prevInterconversionStep(molecule).set(backward_steps[t.step()-1]) 
                else:
                    raise Exception("found IRCStepToken but no idea who it belongs to") 
                
            if t.__class__ == tokentypes.IRCFollowingResultsToken:
                self._forward_route_additional_infos.setEndStructureLabel(_properNaming(t.forward()))
                self._backward_route_additional_infos.setEndStructureLabel(_properNaming(t.backward()))


def _properNaming(label):
    type, number = label
    if type == "DC":
        type = "dDC"
    return (type, number)
