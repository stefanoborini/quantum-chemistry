from application.views.web import plugins
from application import graphstore
from lib import filestorage
from lib import utils
from django import http

from wavemoldb.ordfm import grrm2
import settings

class TransitionStatePotentialEnergyCurvePlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(TransitionStatePotentialEnergyCurvePlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "transitionstatepotentialenergycurve"
    def visibleName(self):
        return "Potential Energy Curve"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return TransitionStatePotentialEnergyCurvePlugin()

class RequestHandler(object):
    def __init__(self):
        pass
    def dispatch(self, request, **args):
        current_uri = args["uri"]
        graph = graphstore.graph()
 
        try:
            transition_state = grrm2.TransitionState.get(graph, current_uri)
        except:
            return None

        ctx = {}

        iconv_start_tuple_list = grrm2.interconversionStartOf(transition_state).getAll() or []
        iconv_end_tuple_list = grrm2.interconversionEndOf(transition_state).getAll() or []
        if len(iconv_start_tuple_list) + len(iconv_end_tuple_list) != 2:
            return None # we have a problem... a transition state must have two links

        if len(iconv_start_tuple_list) == 2:
            iconv_left = iconv_start_tuple_list[0][0]
            iconv_right = iconv_start_tuple_list[1][0]
            energies_left=_getEnergies(iconv_left)
            energies_right=_getEnergies(iconv_right)
            energies = {}
            energies[0] = grrm2.energy(transition_state).get()
            for k,v in sorted(map( lambda x : (-x[0], x[1]), energies_left.items()) + energies_right.items(), key=lambda x: x[0]):
                print k
                energies[k] = v

            end_left = grrm2.interconversionEnd(iconv_left).get()[0]
            end_right = grrm2.interconversionEnd(iconv_right).get()[0]

            energies[min(energies.keys())-1] = grrm2.energy(end_left).get()
            energies[max(energies.keys())+1] = grrm2.energy(end_right).get()
            
            

        else:
            return None
        
        chart_query = http.QueryDict("").copy()
        chart_query.update( {
                "cht": "lxy",
                "chs": "400x400",
                "chd": "t:"+",".join([ str(x[0]) for x in sorted(energies.items(),key=lambda x:x[0])])+"|"+",".join( [str(x[1]) for x in sorted(energies.items(), key=lambda x:x[0])]),
                "chds": str(min(energies.keys()))+","+str(max(energies.keys()))+","+str(min(energies.values()))+","+str(max(energies.values())),
                "chco": "3072F3,ff0000,00aaaa",
                "chls": "2,4,1",
                "chf": "bg,s,F0F0FF",
                "chm": "s,FF0000,0,-1,5|s,0000ff,1,-1,5|s,00aa00,2,-1,5",
                "chxt": "x,y",
                "chxr": "0,"+str(min(energies.keys()))+","+str(max(energies.keys()))+"|1,"+str(min(energies.values()))+","+str(max(energies.values())),
            } )
        ctx["chartUrl"] = "http://chart.apis.google.com/chart?"+chart_query.urlencode()

        iconstorage = filestorage.ResourceIcon(transition_state, settings=settings.filestorage_settings)
        if iconstorage.readable(filestorage.ResourceIcon.STATIC):
            icon_url = iconstorage.url(filestorage.ResourceIcon.STATIC)
        elif iconstorage.readable(filestorage.ResourceIcon.ANIMATED):
            icon_url = iconstorage.url(filestorage.ResourceIcon.ANIMATED)
        else:
            icon_url = None

        ctx["transitionStateIcon"] = icon_url

        iconstorage = filestorage.ResourceIcon(end_left, settings=settings.filestorage_settings)
        if iconstorage.readable(filestorage.ResourceIcon.STATIC):
            icon_url = iconstorage.url(filestorage.ResourceIcon.STATIC)
        elif iconstorage.readable(filestorage.ResourceIcon.ANIMATED):
            icon_url = iconstorage.url(filestorage.ResourceIcon.ANIMATED)
        else:
            icon_url = None

        ctx["leftEndIcon"] = icon_url

        iconstorage = filestorage.ResourceIcon(end_right, settings=settings.filestorage_settings)
        if iconstorage.readable(filestorage.ResourceIcon.STATIC):
            icon_url = iconstorage.url(filestorage.ResourceIcon.STATIC)
        elif iconstorage.readable(filestorage.ResourceIcon.ANIMATED):
            icon_url = iconstorage.url(filestorage.ResourceIcon.ANIMATED)
        else:
            icon_url = None

        ctx["rightEndIcon"] = icon_url

        ctx["leftEndUrl"]="/resources/%7B"+utils.uriToUuid(end_left.uri())+"%7D"
        ctx["rightEndUrl"]="/resources/%7B"+utils.uriToUuid(end_right.uri())+"%7D"
        return ctx

def _getEnergies(iconv):
        energies = {}
        for step in grrm2.interconversionStep(iconv).getAll():
            step = step[0]
            energies[grrm2.stepNumber(step).get()] = grrm2.energy(step).get()

        return energies



def foo():
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
