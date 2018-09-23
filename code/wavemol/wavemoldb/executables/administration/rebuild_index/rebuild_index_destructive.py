#!/usr/bin/env python

import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..","..") ) )
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from lib import indexing
import settings

from application import models
from wavemoldb.ordfm import namespaces
from wavemoldb.ordfm import grrm2
from application import graphstore


def _indexRdfType(graph, indexer):

    indexer.addIndex("is_grrm__molecule", "BOOLEAN")
    indexer.addIndex("is_grrm__equilibrium_structure", "BOOLEAN")
    indexer.addIndex("is_grrm__transition_state", "BOOLEAN")
    indexer.addIndex("is_grrm__barrierless_dissociated", "BOOLEAN")
    indexer.addIndex("is_grrm__barrier_dissociated", "BOOLEAN")
    indexer.addIndex("is_grrm__interconversion_step", "BOOLEAN")
    indexer.addIndex("is_grrm__interconversion", "BOOLEAN")
    indexer.addIndex("is_grrm__run", "BOOLEAN")
    results = graph.query( namespaces.SPARQL_PREFIX+" SELECT ?uri ?type WHERE { ?uri rdf:type ?type . } ")
        
    for res in results:
        indexer.store(res[0], { 
                                "is_grrm__molecule": False,
                                "is_grrm__equilibrium_structure": False,
                                "is_grrm__transition_state": False,
                                "is_grrm__barrierless_dissociated": False,
                                "is_grrm__barrier_dissociated": False,
                                "is_grrm__interconversion_step": False,
                                "is_grrm__interconversion": False,
                                "is_grrm__run": False,
                                })

        try:
            m=grrm2.Molecule.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__molecule" : True})
        except:
            pass
        try:
            m=grrm2.EquilibriumStructure.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__equilibrium_structure" : True})
        except:
            pass
        try:
            m=grrm2.TransitionState.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__transition_state" : True})
        except:
            pass
        try:
            m=grrm2.BarrierlessDissociated.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__barrierless_dissociated" : True})
        except:
            pass
        try:
            m=grrm2.BarrierDissociated.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__barrier_dissociated" : True})
        except:
            pass
        try:
            m=grrm2.InterconversionStep.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__interconversion_step" : True})
        except:
            pass
        try:
            m=grrm2.Interconversion.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__interconversion" : True})
        except:
            pass
        try:
            m=grrm2.Run.get(graph,res[0])
            if m:
                indexer.store(res[0], { "is_grrm__run" : True})
        except:
            pass



def _indexEnergy(graph, indexer):
    indexer.addIndex("grrm__energy", "VARCHAR(255)")
    
    for m in grrm2.Molecule.all(graph):
        energy = grrm2.energy(m).get()
        if energy:
            indexer.store(m.uri(), { "grrm__energy" : float(energy)})

try:

    graph = graphstore.graph()

    indexer = indexing.DbIndex()
    indexer.drop()

    _indexRdfType(graph, indexer)
    _indexEnergy(graph, indexer)
except Exception, e:
    print e
    sys.exit(1)

sys.exit(0)
