from django.shortcuts import render_to_response
from django import http
from django.utils import simplejson
from lib import indexing
from lib import logger

from .. import basecontext
from . import filters

_current_max_limit = 10

class FilterStringError(Exception): pass

def _parseFilterString(filter_string):
    if filter_string is None or len(filter_string) == 0:
        return []

    filter_objects = {}

    filter_data = filter_string.split(",")
    for f_data in filter_data:
        splitted = f_data.split(":")

        if len(splitted) < 3:
            raise FilterStringError("Not enough parameters")

        try:
            order = int(splitted[0])
        except:
            raise FilterStringError("Non-numeric order")

        type_id = splitted[1]
        params = splitted[2:]
        filter_class = filters.fromTypeId(type_id)
        
        if not filter_class:
            raise FilterStringError("Unknown filter "+str(type_id))

        filter_objects[order] = filter_class(*params)

    expected = 0
    filter_list = []
    for k,v in sorted(filter_objects.items()):
        if k != expected:
            raise FilterStringError("Unexpected order")
        expected += 1
        filter_list.append(v)
        
    return filter_list

def _ajax_search_filter(request):
    log = logger.logger("wavemoldb.search")
    try:
        offset = int(request.GET.get('offset',0))
        limit = int(request.GET.get('limit',_current_max_limit))
        filter_string = request.GET.get("filters","")
    except Exception, e:
        log.info(str(__file__)+" : Invalid ajax request : "+str(e.message)) 
        return http.HttpResponseBadRequest("Invalid request")
   
    if limit > _current_max_limit:
        log.info(str(__file__)+" : Excessive ajax request "+str(limit)) 
        return http.HttpResponseForbidden("Request exceeds limits.")

    try:
        filter_list = _parseFilterString(filter_string)
    except FilterStringError, e:
        log.info(str(__file__)+" : Invalid filter string "+e.message) 
        return http.HttpResponseBadRequest("Invalid request")
    except Exception, e:
        log.error(str(__file__)+" : unexpected exception while parsing filter list "+e.message+" : "+str(filter_string))
        return http.HttpResponseServerError()
        
    db_index = indexing.DbIndex()
    results = db_index.allUris()
    # order not important, but we keep it anyway
    for f in filter_list:
        f.apply(results)

    json_response = { "total": results.count(), 
                      "uri_list" : [],
                      "offset" : offset,
                      "limit" : limit,
                    }

    results.limit(limit).offset(offset)
    for r in results:
        json_response["uri_list"].append( r[0] )

    return http.HttpResponse(simplejson.dumps(json_response), mimetype='application/javascript')

def render(request):
    if request.method == "GET" and request.GET:
        if request.GET.get("type", None) == "ajax":
            return _ajax_search_filter(request)
    return render_to_response('application/search.html', { "base" : basecontext.context() }) 
