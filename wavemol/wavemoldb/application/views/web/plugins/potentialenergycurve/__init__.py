from application.views.web import plugins
from application import graphstore
from lib import filestorage
from lib import utils
from django import http

from wavemoldb.ordfm import grrm2
import settings

class PotentialEnergyCurvePlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(PotentialEnergyCurvePlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "potentialenergycurve"
    def visibleName(self):
        return "Potential Energy Curve"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return PotentialEnergyCurvePlugin()

class RequestHandler(object):
    def __init__(self):
        pass
    def dispatch(self, request, **args):
        current_uri = args["uri"]
        graph = graphstore.graph()
 
        try:
            route = grrm2.Interconversion.get(graph, current_uri)
        except:
            return None

        start = grrm2.interconversionStart(route).get()[0]
        end = grrm2.interconversionEnd(route).get()[0]
        
        iconstorage_start = filestorage.ResourceIcon(start, settings=settings.filestorage_settings)
        iconstorage_end = filestorage.ResourceIcon(end, settings=settings.filestorage_settings)
        iconstorage_route = filestorage.ResourceIcon(route, settings=settings.filestorage_settings)

        ctx = {}
        ctx["startUrl"] = "/resources/%7B"+utils.uriToUuid(start.uri())+"%7D"
        ctx["endUrl"] = "/resources/%7B"+utils.uriToUuid(end.uri())+"%7D"
        ctx["startIcon"] = iconstorage_start.url(filestorage.ResourceIcon.STATIC)
        ctx["endIcon"] = iconstorage_end.url(filestorage.ResourceIcon.STATIC)
        ctx["connectionRouteIcon"] = iconstorage_route.url(filestorage.ResourceIcon.ANIMATED)

        ctx["startStructureLabel"] = _getLabel(start)
        ctx["endStructureLabel"] = _getLabel(end)
    
        energies = {}
        for step in grrm2.interconversionStep(route).getAll():
            step = step[0]
            energies[grrm2.stepNumber(step).get()] = grrm2.energy(step).get()

        energies[0] = grrm2.energy(start).get()
        energies[max(energies.keys())+1] = grrm2.energy(end).get()

        chart_query = http.QueryDict("").copy()
        chart_query.update( {
                "cht": "lxy",
                "chs": "400x400",
                "chd": "t:"+",".join([ str(x) for x in energies.keys()])+"|"+",".join( [str(x) for x in energies.values()]),
                "chds": str(min(energies.keys()))+","+str(max(energies.keys()))+","+str(min(energies.values()))+","+str(max(energies.values())),
                "chco": "3072F3,ff0000,00aaaa",
                "chls": "2,4,1",
                "chf": "bg,s,F0F0FF",
                "chm": "s,FF0000,0,-1,5|s,0000ff,1,-1,5|s,00aa00,2,-1,5",
                "chxt": "x,y",
                "chxr": "0,"+str(min(energies.keys()))+","+str(max(energies.keys()))+"|1,"+str(min(energies.values()))+","+str(max(energies.values())),
            } )
        ctx["chartUrl"] = "http://chart.apis.google.com/chart?"+chart_query.urlencode()


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
