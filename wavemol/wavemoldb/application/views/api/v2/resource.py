from django import http

from lib import utils
from lib import logger
from wavemoldb import ordfm
from application import graphstore
import rdflib

def render(request, resource_uuid):
    log = logger.logger("wavemoldb.api")
    try:
        resource_uri = utils.uuidToUri(resource_uuid)
    except:
        log.info("Invalid resource uuid "+str(resource_uuid))
        raise http.Http404

    g=rdflib.ConjunctiveGraph()
    for p,o in graphstore.graph().predicate_objects(rdflib.URIRef(resource_uri)):
        if type(o) == rdflib.BNode:
            dumpBNode(graphstore.graph(), o, g)
        g.add( (rdflib.URIRef(resource_uri),p,o) )
    for s,p in graphstore.graph().subject_predicates(rdflib.URIRef(resource_uri)):
        if type(s) == rdflib.BNode:
            dumpBNode(graphstore.graph(), s, g)
        g.add( (s, p, rdflib.URIRef(resource_uri)) )
    
    response = http.HttpResponse(g.serialize(), mimetype="text/xml")
    return response

def dumpBNode(maingraph, bnode, finalgraph):
    for p,o in maingraph.predicate_objects(bnode):
        if type(o) == rdflib.BNode:
            dumpBNode(maingraph, o, finalgraph)
        finalgraph.add( (bnode, p, o) )

    for s,p in maingraph.subject_predicates(bnode):
        if type(s) == rdflib.BNode:
            dumpBNode(maingraph, s, finalgraph)
        finalgraph.add( (s, p, bnode) )

