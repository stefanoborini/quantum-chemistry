from django import template
from django.template import loader
from django import http
import sys

from application.views.web import basecontext
import plugins 
from lib import utils
from lib import logger
from wavemoldb.ordfm import grrm2
from application import graphstore

import traceback

def render(request, resource_uuid):
    log=logger.logger("wavemoldb")
    try:
        resource_uri = utils.uuidToUri(resource_uuid)
    except Exception, e:
        log.info(str(__file__)+" : Unable to convert to uri "+str(resource_uuid)+" "+e.message)
        raise http.Http404()

    graph = graphstore.graph()
    if not grrm2.Thing.get(graph, resource_uri):
        log.info(str(__file__)+" : not found "+str(resource_uri))
        raise http.Http404

    registry = plugins.PluginRegistry()

    all_plugins = registry.allPlugins()

    if request.method == "GET" and request.GET and request.GET["type"] == "ajax" and request.GET.get("receiver_plugin"):
        for p in registry.allPlugins():
            if p.ajaxHandlerGet() is not None and p.name() == request.GET.get("receiver_plugin"):
                response = p.ajaxHandlerGet().dispatch(request, uri=resource_uri)
                if response is not None:
                    return response
                else:
                    raise http.Http404
        raise http.Http404

    ctx={} 
    ctx["base"] = basecontext.context()
    ctx["resource"] = {}
    ctx["resource"]["uuid"] = utils.uriToUuid(resource_uri)
    ctx["resource"]["uri"] = resource_uri
    ctx["plugins"] = []
    ctx["pluginContext"] = {}
    
    for p in registry.allPlugins():
        try:
            plugin_ctx = p.requestHandler().dispatch(request, uri=resource_uri)
        except Exception, e:
            log.warning(str(__file__)+" : Plugin "+p.name()+" raised exception : "+e.message+" : "+str(traceback.print_tb(sys.exc_traceback)))
            plugin_ctx = None
        if plugin_ctx is not None:
            ctx["plugins"].append(p)
            ctx["pluginContext"][p.name()] = plugin_ctx

    t = loader.get_template("application/resource.html")
     
    c = template.Context(ctx)
    return http.HttpResponse(t.render(c))

