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
            if request.GET["type"] == "ajax" and request.GET["receiver_plugin"] == "runoutput":
                if request.GET.get("method") == "getTableData":
                    return self._getTableData(request,uri)
                elif request.GET.get("method") == "getUris":
                    return self._getUris(request,uri)
        return None 

    def _getUris(self, request, uri):
        graph = graphstore.graph()
        try:
            run = grrm2.Run.get(graph, uri)
        except:
            raise http.Http404

        try:
            offset = int(request.GET["offset"])
        except:
            offset = 0

        try:
            limit = int(request.GET["limit"])
        except:
            limit = 10

        output={}
        output["uri_list"] = []
        output["resource_type"] = []
    
        output["total"] = len(grrm2.runOutput(run).get())
        output["offset"] = offset
        output["limit"] = limit

        for output_tuple in grrm2.runOutput(run).get().limit(limit).offset(offset):
            resource = output_tuple[0]
            output["uri_list"].append(resource.uri())

            if grrm2.TransitionState.tryCast(resource):
                resource_type = "TransitionState"
            elif grrm2.EquilibriumStructure.tryCast(resource):
                resource_type = "EquilibriumStructure"
            elif grrm2.EquilibriumStructure.tryCast(resource):
                resource_type = "EquilibriumStructure"
            elif grrm2.BarrierDissociated.tryCast(resource):
                resource_type = "BarrierDissociated"
            elif grrm2.BarrierlessDissociated.tryCast(resource):
                resource_type = "BarrierlessDissociated"
            elif grrm2.Interconversion.tryCast(resource):
                resource_type = "Interconversion"
            elif grrm2.InterconversionStep.tryCast(resource):
                resource_type = "InterconversionStep"
            else:
                resource_type = "Thing"
            output["resource_type"].append(resource_type)

        return http.HttpResponse(simplejson.dumps(output), mimetype='application/javascript')

    def _getTableData(self,request,uri):
        try:
            uris = request.GET.getlist("uris")
#            page = int(request.POST['page'])
#            rows_per_page = int(request.POST['rp'])
#            sortname = request.POST['sortname']
#            sortorder = request.POST['sortorder']
        except:
            return http.HttpResponseBadRequest()
       
        json_response = {}
        json_response["rows"] = []
        for uri in uris:
            resclass = ordfm.classByUri(graphstore.graph(),uri)
            resource = resclass.get(graphstore.graph(),uri)
            storage = filestorage.ResourceStorage(resource, web_accessible=True, settings=settings.filestorage_settings)
            iconstorage = filestorage.ResourceIcon(resource, settings=settings.filestorage_settings)

            row = {}
            row["icon"] = iconstorage.url(filestorage.ResourceIcon.STATIC)
            row["animatedicon"] = iconstorage.url(filestorage.ResourceIcon.ANIMATED)
            row["uri"] = uri
            row["url"] = utils.resourceUrl(resource)
            row["type"] = resclass.visibleName()
            json_response["rows"].append(row)


#        if page < 0:
#            return http.HttpResponseBadRequest("Invalid page number")
#
#        graph = graphstore.graph()
#        c = ordfm.Collection.get(graph, uri)
#
#        json_response = { "page": page, 
#                          "total": len(c.contents()), 
#                          "rows" : []
#                        }
#
#        for m_uri in c.contents().values()[(page-1)*rows_per_page:(page-1)*rows_per_page+rows_per_page]:
#            m = ordfm.Molecule.get(graph, m_uri)
#            json_response["rows"].append( { "cell" : [ "<span style=\"font-family: Courier\"><a href=\"/molecules/{"+utils.uriToUuid(m_uri)+"}\">"+utils.uriToUuid(m_uri)+"</a></span>", "", m.formula(), str(m.structureType()), str(m.energy()) ] } )
        return http.HttpResponse(simplejson.dumps(json_response), mimetype='application/javascript')

class RequestHandler(object):
    def __init__(self):
        pass

    def dispatch(self, request, **args):
        graph = graphstore.graph()
        try:
            run = grrm2.Run.get(graph, args["uri"])
        except:
            return None

        return { "resource_uuid" : utils.uriToUuid(run.uri())}

class RunOutputPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(RunOutputPlugin, self).__init__()
        self._ajax_handler = None
        self._request_handler = None
    def name(self):
        return "runoutput"
    def visibleName(self):
        return "Output"
    def ajaxHandlerGet(self):
        if self._ajax_handler == None:
            self._ajax_handler = AjaxHandlerGet()
        return self._ajax_handler
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return RunOutputPlugin()

