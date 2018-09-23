from application.views.web import plugins
from application import graphstore
from lib import filestorage
from lib import utils

from wavemoldb.ordfm import grrm2
import settings

class InterconversionStepsPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(InterconversionStepsPlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "interconversionsteps"
    def visibleName(self):
        return "Interconversion Steps"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return InterconversionStepsPlugin()


class StepInfo(object):
    def __init__(self):
        self.number = None
        self.uri = None
        self.link = None
        self.icon = None
        self.label = None

class ResultInfo(object):
    def __init__(self):
        self.uri = None
        self.link = None
        self.icon = None
        self.label = None

class RequestHandler(object):
    def __init__(self):
        pass
    def dispatch(self, request, **args):
        current_uri = args["uri"]
        graph = graphstore.graph()
 
        try:
            iconv = grrm2.Interconversion.get(graph, current_uri)
        except:
            return None

        ctx = {}

        ctx["steps"] = []
        ctx["start"] = ResultInfo()
        ctx["end"] = ResultInfo()

        start = grrm2.interconversionStart(iconv).get()[0]
        ctx["start"].uri = start.uri()
        ctx["start"].link = "/resources/%7B"+utils.uriToUuid(start.uri())+"%7D"
        iconstorage = filestorage.ResourceIcon(start, settings=settings.filestorage_settings)
        ctx["start"].icon = iconstorage.url(filestorage.ResourceIcon.STATIC)
        ctx["start"].energy = grrm2.energy(start).get()
        ctx["start"].label = _getLabel(start)

        end = grrm2.interconversionEnd(iconv).get()[0]
        ctx["end"].uri = end.uri()
        ctx["end"].link = "/resources/%7B"+utils.uriToUuid(end.uri())+"%7D"
        iconstorage = filestorage.ResourceIcon(end, settings=settings.filestorage_settings)
        ctx["end"].icon = iconstorage.url(filestorage.ResourceIcon.STATIC)
        ctx["end"].energy = grrm2.energy(end).get()
        ctx["end"].label = _getLabel(end)

        for s in grrm2.interconversionStep(iconv).getAll():
            step = s[0]
            iconstorage = filestorage.ResourceIcon(step, settings=settings.filestorage_settings)
            info = StepInfo()
            info.link = "/resources/%7B"+utils.uriToUuid(step.uri())+"%7D"
            info.icon = iconstorage.url(filestorage.ResourceIcon.STATIC)
            info.uri = step.uri()
            info.energy = grrm2.energy(step).get()
            info.number = grrm2.stepNumber(step).get()
            ctx["steps"].append(info)

        def cmpFunc(x,y):
            return cmp(x.number, y.number) 
        ctx["steps"] = sorted(ctx["steps"], cmp=cmpFunc) 



        return ctx

def _getLabel(molecule):
    label = "Unknown"
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

        label = struct_type+str(struct_number)

    return label
