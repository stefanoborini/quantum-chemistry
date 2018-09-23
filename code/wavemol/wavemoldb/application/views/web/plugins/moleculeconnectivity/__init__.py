from lib import utils
from lib import filestorage
from application.views.web import plugins
from application import graphstore

from wavemoldb.ordfm import grrm2


import settings

class RouteInfo(object):
    def __init__(self):
        self.targetLink = None
        self.targetIcon = None
        self.targetStructureLabel = None
        self.targetEnergy = None

        self.energyDifference = None
        self.icon = None
        self.numSteps = None
        self.link = None

class MoleculeInfo(object):
    def __init__(self):
        self.icon = None
        self.structureLabel = None
        self.isInterconversionStep = None
    def __repr__(self):
        return self.structureLabel
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

        context["moleculeInfo"] = self._getMoleculeInfo(molecule)

        if context["moleculeInfo"].isInterconversionStep:
            interconversion_step = grrm2.InterconversionStep.tryCast(molecule)
            prev_step = grrm2.prevInterconversionStep(interconversion_step).get()
            next_step = grrm2.nextInterconversionStep(interconversion_step).get()

            interconversion = grrm2.interconversionStepOf(interconversion_step).get()
            if interconversion and interconversion[0]:
                start_structure = grrm2.interconversionStart(interconversion[0]).get()
                if start_structure and start_structure[0]:
                    start_structure = start_structure[0]

                end_structure = grrm2.interconversionEnd(interconversion[0]).get()
                if end_structure and end_structure[0]:
                    end_structure = end_structure[0]

            if prev_step and prev_step[0]:
                context["prevStepInfo"] = self._getMoleculeInfo(prev_step[0])
            else:
                context["prevStepInfo"] = self._getMoleculeInfo(start_structure)

            if next_step and next_step[0]:
                context["nextStepInfo"] = self._getMoleculeInfo(next_step[0])
            else:
                context["nextStepInfo"] = self._getMoleculeInfo(end_structure)
            
        else:
            context["isInterconversion"] = False
            context["fromRoutes"] = self._getFromRoutesContext(molecule)
            context["toRoutes"] = self._getToRoutesContext(molecule)

        return context

    def _getMoleculeInfo(self, molecule):
        info = MoleculeInfo()

        info.icon = filestorage.ResourceIcon(molecule, settings=settings.filestorage_settings).url(filestorage.ResourceIcon.STATIC)
        info.link = "/resources/%7B"+utils.uriToUuid(molecule.uri())+"%7D"
        info.structureLabel = "Unknown"
        info.isInterconversionStep = False

        interconversion_step = grrm2.InterconversionStep.tryCast(molecule)
        icresult = grrm2.InterconversionResult.tryCast(molecule)
        if interconversion_step:
            info.isInterconversionStep = True
            info.structureLabel = "IC - step "+str(grrm2.stepNumber(interconversion_step).get())
        elif icresult:
            struct_number = grrm2.structureNumber(icresult).get()
            if grrm2.EquilibriumStructure.tryCast(icresult):
                struct_type = "EQ"
            elif grrm2.TransitionState.tryCast(icresult):
                struct_type = "TS"
            elif grrm2.BarrierlessDissociated.tryCast(icresult):
                struct_type = "DDC"
            elif grrm2.BarrierDissociated.tryCast(icresult):
                struct_type = "UDC"

            info.structureLabel = struct_type+str(struct_number)

        return info
    def _getFromRoutesContext(self, molecule):

        icres=grrm2.InterconversionResult.tryCast(molecule)

        context = []
        iconvs = grrm2.interconversionEndOf(icres).getAll()
        if iconvs is None:
            return context

        for iconv in iconvs:
            iconv = iconv[0]
            start = grrm2.interconversionStart(iconv).get()[0]
            

            route_info = RouteInfo()
            route_info.link = "/resources/%7B"+utils.uriToUuid(iconv.uri())+"%7D"

            route_info.targetLink = "/resources/%7B"+utils.uriToUuid(start.uri())+"%7D"
            route_info.targetIcon = filestorage.ResourceIcon(start, settings=settings.filestorage_settings).url(filestorage.ResourceIcon.STATIC)
            struct_number = grrm2.structureNumber(start).get()
            if grrm2.EquilibriumStructure.tryCast(start):
                struct_type = "EQ"
            elif grrm2.TransitionState.tryCast(start):
                struct_type = "TS"
            elif grrm2.BarrierlessDissociated.tryCast(start):
                struct_type = "DDC"
            elif grrm2.BarrierDissociated.tryCast(start):
                struct_type = "UDC"

            route_info.targetStructureLabel = struct_type+str(struct_number)
            route_info.targetEnergy = grrm2.energy(start).get()

            route_info.energyDifference = grrm2.energy(start).get() - grrm2.energy(molecule).get()

            route_info.icon=filestorage.ResourceIcon(iconv, settings=settings.filestorage_settings).url(filestorage.ResourceIcon.ANIMATED)

            context.append(route_info)

        return context

    def _getToRoutesContext(self, molecule):
        icres=grrm2.InterconversionResult.tryCast(molecule)

        context = []
        iconvs = grrm2.interconversionStartOf(icres).getAll()
        if iconvs is None:
            return context
        for iconv in iconvs:
            iconv = iconv[0]
            end = grrm2.interconversionEnd(iconv).get()[0]
            

            route_info = RouteInfo()
            route_info.link = "/resources/%7B"+utils.uriToUuid(iconv.uri())+"%7D"

            route_info.targetLink = "/resources/%7B"+utils.uriToUuid(end.uri())+"%7D"
            route_info.targetIcon = filestorage.ResourceIcon(end, settings=settings.filestorage_settings).url(filestorage.ResourceIcon.STATIC)
            struct_number = grrm2.structureNumber(end).get()
            if grrm2.EquilibriumStructure.tryCast(end):
                struct_type = "EQ"
            elif grrm2.TransitionState.tryCast(end):
                struct_type = "TS"
            elif grrm2.BarrierlessDissociated.tryCast(end):
                struct_type = "DDC"
            elif grrm2.BarrierDissociated.tryCast(end):
                struct_type = "UDC"

            route_info.targetStructureLabel = struct_type+str(struct_number)
            route_info.targetEnergy = grrm2.energy(end).get()

            route_info.energyDifference = grrm2.energy(end).get() - grrm2.energy(molecule).get()

            route_info.icon=filestorage.ResourceIcon(iconv, settings=settings.filestorage_settings).url(filestorage.ResourceIcon.ANIMATED)

            context.append(route_info)

        return context


class MoleculeConnectivityPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(MoleculeConnectivityPlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "moleculeconnectivity"
    def visibleName(self):
        return "Connections"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return MoleculeConnectivityPlugin()
