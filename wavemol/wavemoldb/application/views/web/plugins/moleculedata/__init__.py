from lib import utils
from lib import chemistry
from lib import filestorage
from application.views.web import plugins
from application import graphstore

from wavemoldb.ordfm import grrm2
import settings

class RequestHandler(object):
    def __init__(self):
        pass

    def dispatch(self, request, uri):
        context = {}
        graph = graphstore.graph()

        try:
            molecule = grrm2.Molecule.get(graph, uri)
        except:
            return None

        context["moleculeInfo"] = []
        context["moleculeInfo"].append( ("Formula",grrm2.hillFormula(molecule).get(), None) )
        context["moleculeInfo"].append( ("Molecular Mass", grrm2.mass(molecule).get(), None) )
        context["moleculeInfo"].append( ("InChi", grrm2.inchi(molecule).get(), None) )
        context["moleculeInfo"].append( ("SMILES", grrm2.smiles(molecule).get(), None) )
        context["moleculeInfo"].append( ("Energy", grrm2.energy(molecule).get(), None) )
        context["moleculeInfo"].append( ("Charge", grrm2.charge(molecule).get(), None) )
        context["moleculeInfo"].append( ("Spin", grrm2.spin(molecule).get(), None) )

        context["moleculeInfo"].append( ("Structure Type", _getStructureType(molecule), None) )

        result = grrm2.InterconversionResult.tryCast(molecule)
        if result:
            context["moleculeInfo"].append( ("Structure Number", grrm2.structureNumber(result).get(), None) )
            context["moleculeInfo"].append( ("Zero Point Vibrational Energy", grrm2.zeroPointVibrationalEnergy(result).get(), None) )

        step = grrm2.InterconversionStep.tryCast(molecule)
        if step:
            context["moleculeInfo"].append( ("Interconversion Step", grrm2.stepNumber(step).get(), None) )
            context["moleculeInfo"].append( ("Belongs to interconversion", grrm2.interconversionStepOf(step).get()[0].uri(), "/resources/%7B"+utils.uriToUuid(grrm2.interconversionStepOf(step).get()[0].uri())+"%7D") )
            

        context["moleculeInfo"].append(("CANOST canonical planar", grrm2.canostSerialCanonical(molecule).get(), None) )
        context["moleculeInfo"].append(("CANOST canonical serial", grrm2.canostPlanarCanonical(molecule).get(), None) )

        context["moleculeInfo"].append(("CANOST planar codes", grrm2.canostPlanar(molecule).get(), None) )
        context["moleculeInfo"].append(("CANOST serial codes", grrm2.canostSerial(molecule).get(), None) )

        fragment_strings = []
        if grrm2.fragments(molecule).get() is not None:
            geometry = grrm2.geometry(molecule).get()
            for fragment in grrm2.fragments(molecule).get():
                symbols = [geometry["symbols"][i-1] for i in fragment] 
                fragment_strings.append(chemistry.hillFormula(symbols))
                
        context["moleculeInfo"].append(("Fragments", "/".join(fragment_strings), None) )

        try:
            run=grrm2.runOutputOf(molecule).get()[0]
            context["moleculeInfo"].append( ( "Run", run.uri(), "/resources/%7B"+utils.uriToUuid(run.uri())+"%7D"))
        except Exception, e:
            pass

        try:
            run=grrm2.runInputOf(molecule).get()[0]
            context["moleculeInfo"].append( ( "Run", run.uri(), "/resources/%7B"+utils.uriToUuid(run.uri())+"%7D"))
        except:
            pass
    

        return context



def _getStructureType(molecule):
    if grrm2.EquilibriumStructure.tryCast(molecule):
        return "Equilibrium Structure"
    elif grrm2.TransitionState.tryCast(molecule):
        return "Transition State"
    elif grrm2.BarrierlessDissociated.tryCast(molecule):
        return "Barrierless Dissociated"
    elif grrm2.BarrierDissociated.tryCast(molecule):
        return "Barrier Dissociated"
    elif grrm2.InterconversionStep.tryCast(molecule):
        return "Interconversion Structure"
    else:
        return "Molecule"

class MoleculeDataPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(MoleculeDataPlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "moleculedata"
    def visibleName(self):
        return "Molecule Information"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return MoleculeDataPlugin()
