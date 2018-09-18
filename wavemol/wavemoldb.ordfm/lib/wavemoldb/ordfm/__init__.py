import rdflib
import simplejson
from . import namespaces
import urlparse

import sys
import inspect

##############################################################
class ThingResultProxy(object):
    def __init__(self, cls, graph):
        self._cls = cls
        self._clslist = [cls] + list(cls.subclasses())
        self._graph = graph
        self._limit = None
        self._offset = None
        self._query = None
    def offset(self, offset):
        self._offset = offset
        return self
    def limit(self, limit):
        self._limit = limit
        return self
    def __iter__(self):
        if not self._query:  
            self._doQuery()
        return self
    def __len__(self):
        if not self._query:
            self._doQuery()
        return len(self._query)        
    def _doQuery(self):
        query_add = ""
        query_string = "SELECT ?uri WHERE { "
        if len(self._clslist) > 1:
            query_string += " UNION ".join([ " { ?uri "+str(rdflib.RDF.type.n3())+" "+str(x.typeUri().n3())+" . } " for x in self._clslist] )
        else:
            query_string += " ?uri "+str(rdflib.RDF.type.n3())+" "+str(self._clslist[0].typeUri().n3())+" . "
        query_string += " } " 
        if self._limit:
            query_string += " LIMIT "+str(self._limit)
        if self._offset:
            query_string += " OFFSET "+str(self._offset)
        self._query = self._graph.query(query_string)
        self._iterator = iter(self._query)
    def next(self):
        if not self._query:
            self._doQuery()
        n = self._iterator.next()
        return self._cls(self._graph,rdflib.URIRef(n[0]))

class ThingObject(object):
    def __init__(self, graph, uri):
        self._graph = graph
        self._uri = uri
    @classmethod
    def new(cls, graph, uri):
        tri = graph.triples( ( rdflib.URIRef(uri), rdflib.RDF.type, cls.typeUri()) )
        try:
            tri.next()
            raise Exception(str(uri)+" already existent")
        except StopIteration:
            pass
         
        graph.add( ( rdflib.URIRef(uri), rdflib.RDF.type, cls.typeUri()) )
        return cls.get(graph, rdflib.URIRef(uri))
    @classmethod
    def all(cls, graph):
        return ThingResultProxy(cls, graph)

    @classmethod
    def get(cls, graph, uri):
        # basic get, based on rdf:type, no reasoner
        po = graph.predicate_objects(subject = rdflib.URIRef(uri))
        try:
            po.next()
        except StopIteration:
            return None

        for t in graph.objects(subject = rdflib.URIRef(uri), predicate=rdflib.RDF.type):
            if t in [ x.typeUri() for x in [ cls ] + list(cls.subclasses())]:
                return cls(graph, uri)
        
        raise Exception("getting an invalid type")
    def graph(self):
        return self._graph
    def uri(self):
        return self._uri
    @classmethod
    def visibleName(cls):
        return cls.__name__
    @classmethod
    def codeFriendlyName(cls):
        return cls.__name__
    @classmethod
    def tryCast(cls, object):
        try:
            return cls.get(object.graph(), object.uri())
        except:
            pass
        return None

class DataProperty(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        if not all([d.get(self._graph, self._subject) for d in self.domain()]):
            raise Exception("domain violation for uri "+str(self._subject))
    def get(self):
        literal = self._graph.value( subject=self._subject, predicate=self.propertyUri(), any=False)
        if literal:
            return self.range()(literal)
        return None
    def set(self, literal):
        try:
            value = self.range()(literal)
        except:
            raise Exception("range violation for literal "+str(literal))
        self._graph.set( (rdflib.URIRef(self._subject), self.propertyUri(), rdflib.Literal(value)))

class ObjectProperty(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def get(self):
        ret = None
        others = self._graph.objects( subject=self._subject, predicate=self.propertyUri())
        for o in others:
            if ret:
                raise Exception("Uniqueness violation in db")
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated for uri "+str(o))
            ret = tuple(instances)
        return ret 
    def set(self, other):
        if self._graph != other.graph():
            raise Exception("different graphs")
        try:
            [d.get(self._graph, other.uri()) for d in self.range()]
        except:
            raise Exception("range violation")
        self._graph.set( (rdflib.URIRef(self._subject), self.propertyUri(), rdflib.URIRef(other.uri())))

class MultipleObjectProperty(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def getAll(self):
        ret = []
        others = self._graph.objects( subject=self._subject, predicate=self.propertyUri())
        for o in others:
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            ret.append(tuple(instances))
        return ret 
    def get(self):
        return MultipleObjectPropertyResultProxy(self, self._graph) 
    def add(self, other):
        if self._graph != other.graph():
            raise Exception("different graphs")
        try:
            [d.get(self._graph, other.uri()) for d in self.range()]
        except:
            raise Exception("range violation")
        self._graph.add( (rdflib.URIRef(self._subject), self.propertyUri(), rdflib.URIRef(other.uri())) )
    def subject(self):
        return self._subject

class MultipleObjectPropertyResultProxy(object):
    def __init__(self, property, graph):
        self._property = property
        self._graph = graph
        self._limit = None
        self._offset = None
        self._query = None
    def offset(self, offset):
        if self._query: 
            raise Exception("Already queried")
        self._offset = offset
        return self
    def limit(self, limit):
        if self._query: 
            raise Exception("Already queried")
        self._limit = limit
        return self
    def __iter__(self):
        if not self._query:  
            self._doQuery()
        return self
    def __len__(self):
        if not self._query:
            self._doQuery()
        return len(self._query)        
    def _doQuery(self):
        query_string = "SELECT ?o WHERE { "
        query_string += str(self._property.subject().n3())+" "+str(self._property.propertyUri().n3())+" ?o . "
        query_string += " } " 
        if self._limit:
            query_string += " LIMIT "+str(self._limit)
        if self._offset:
            query_string += " OFFSET "+str(self._offset)
        self._query = self._graph.query(query_string)
        self._iterator = iter(self._query)
    def next(self):
        if not self._query:
            self._doQuery()
        n = self._iterator.next()
        instances = [d.get(self._graph, n[0]) for d in self._property.range()]
        return tuple(instances)

#############################################################

class OriginalSubmission(ThingObject): 
    @staticmethod
    def subclasses():
        return set([])
    @staticmethod
    def superclasses():
        return set([])
    @staticmethod
    def typeUri():
        return namespaces.WMOLDB_NS.OriginalSubmission

class SystemSubmission(ThingObject): 
    @staticmethod
    def subclasses():
        return set([])
    @staticmethod
    def superclasses():
        return set([])
    @staticmethod
    def typeUri():
        return namespaces.WMOLDB_NS.SystemSubmission
