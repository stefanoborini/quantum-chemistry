from django.shortcuts import render_to_response
from django import http
from django.utils import simplejson
from lib import indexing
from lib import logger
from lib import utils
from lib import filestorage
from django import template
from django.template import loader
from django import http
import sys
import settings

from application.views.web import basecontext
from lib import utils
from lib import logger
from wavemoldb.ordfm import grrm2
from application import graphstore

from .. import basecontext
from . import filters

def render(request,resource_uuid):
    log=logger.logger("wavemoldb")
    try:
        resource_uri = utils.uuidToUri(resource_uuid)
    except Exception, e:
        log.info(str(__file__)+" : Unable to convert to uri "+str(resource_uuid)+" "+e.message)
        print str(__file__)+" : Unable to convert to uri "+str(resource_uuid)+" "+e.message
        raise http.Http404()

    graph = graphstore.graph()
    try:
        thing = grrm2.Thing.get(graph, resource_uri)
    except:
        log.info(str(__file__)+" : not found "+str(resource_uri))
        raise http.Http404
        
    if not thing:
        log.info(str(__file__)+" : not found "+str(resource_uri))
        raise http.Http404

    iconstorage = filestorage.ResourceIcon(thing, settings=settings.filestorage_settings)
    if iconstorage.readable(filestorage.ResourceIcon.STATIC):
        icon_url = iconstorage.url(filestorage.ResourceIcon.STATIC)
    elif iconstorage.readable(filestorage.ResourceIcon.ANIMATED):
        icon_url = iconstorage.url(filestorage.ResourceIcon.ANIMATED)
    else:
        icon_url = None

    resource_type = None
    if grrm2.Run.tryCast(thing):
        resource_type = "Run"
    elif grrm2.TransitionState.tryCast(thing):
        resource_type = "TransitionState"
    elif grrm2.EquilibriumStructure.tryCast(thing):
        resource_type = "EquilibriumStructure"
    elif grrm2.BarrierDissociated.tryCast(thing):
        resource_type = "BarrierDissociated"
    elif grrm2.BarrierlessDissociated.tryCast(thing):
        resource_type = "BarrierlessDissociated"
    elif grrm2.InterconversionStep.tryCast(thing):
        resource_type = "InterconversionStep"
    elif grrm2.Interconversion.tryCast(thing):
        resource_type = "Interconversion"
    elif grrm2.RunInput.tryCast(thing):
        resource_type = "RunInput"
    else:
        resource_type = "Thing"

    return render_to_response('application/searchsnippets.html', { "base" : basecontext.context() , "resource_uuid" : utils.uriToUuid(resource_uri), "resource_type": resource_type, "icon_url": icon_url}) 
