from application.views.web import plugins
from django import http
from django.utils import simplejson
import settings

from lib import utils
from lib import filestorage
from wavemoldb import ordfm
from wavemoldb.ordfm import grrm2
from application import graphstore

class AjaxHandlerGet(object):
    def __init__(self): pass

    def dispatch(self, request, **args):
        uri = args["uri"]
        if request.method == "GET" and request.GET:
            if request.GET["type"] == "ajax" and request.GET["receiver_plugin"] == "connectivity":
                if request.GET.get("method") == "getInterconversionEnergy":
                    return self._getInterconversionEnergy(request,uri, request.GET.get("interconversion_uuid"))
        return None 

    def _getInterconversionEnergy(self, request, uri, interconversion_uuid):
        graph = graphstore.graph()
        try:
            route = grrm2.Interconversion.get(graph, utils.uuidToUri(interconversion_uuid))
        except:
            raise http.Http404

        output={}

        start = grrm2.interconversionStart(route).get()[0]
        end = grrm2.interconversionEnd(route).get()[0]
        
        energies = {}
        for step in grrm2.interconversionStep(route).getAll():
            step = step[0]
            energies[grrm2.stepNumber(step).get()] = grrm2.energy(step).get()

        energies[0] = grrm2.energy(start).get()
        energies[max(energies.keys())+1] = grrm2.energy(end).get()

        output["energies"] = energies
    
        return http.HttpResponse(simplejson.dumps(output), mimetype='application/javascript')

class RequestHandler(object):
    def __init__(self):
        pass

    def dispatch(self, request, **args):
        graph = graphstore.graph()
        try:
            run = grrm2.Run.get(graph, args["uri"])
        except:
            return None

        storage = filestorage.ResourceStorage(run, web_accessible=True, settings=settings.filestorage_settings)
        return { "connectivityUrl" : settings.HOST_BASE+storage.url("connectivity", "csv"), "resource_uuid" : utils.uriToUuid(run.uri())}

class ConnectivityPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(ConnectivityPlugin, self).__init__()
        self._ajax_handler = None
        self._request_handler = None
    def name(self):
        return "connectivity"
    def visibleName(self):
        return "Connectivity"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler
    def ajaxHandlerGet(self):
        if self._ajax_handler == None:
            self._ajax_handler = AjaxHandlerGet()
        return self._ajax_handler

def init():
    return ConnectivityPlugin()

