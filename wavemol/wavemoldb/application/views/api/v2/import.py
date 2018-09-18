from django import http
import StringIO
import rdflib

from application import models
from lib import uuid
from lib import filestorage
from lib import logger
import settings


def dispatch(request):
    log = logger.logger("wavemoldb.api")

    if request.method != "POST":
        log.info("Invalid import request from "+str(request.get_host())+" : not POST request")
        return http.HttpResponseBadRequest("Accepting POST")
    try:
        xml = request.POST["xml"]
    except:
        log.info("Invalid import request from "+str(request.get_host())+" : xml parameter missing")
        return http.HttpResponseBadRequest("xml parameter missing")

    g=rdflib.ConjunctiveGraph()
    g.parse(StringIO.StringIO(xml))

    fs = filestorage.FileStorage("importer", web_accessible=False, settings=settings.filestorage_settings)
    identifier = str(uuid.uuid4())
    path = fs.path(identifier+".rdf")
    f=open(path,"w")
    f.write(g.serialize())
    f.close()
    
    q=models.QueuedTask(type="import",parameters=identifier,status="QUEUED")
    q.save()
    log.info("Accepted submission "+str(identifier)+" from "+str(request.get_host()))

    return http.HttpResponse(status=202)
