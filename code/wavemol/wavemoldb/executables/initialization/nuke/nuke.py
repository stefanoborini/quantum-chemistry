#!/usr/bin/env python

import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..","..") ) )
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

from lib import indexing
from wavemoldb.ordfm import namespaces
import settings
import rdflib
from rdflib import store
import time

from application import models

    
print "This program destroys the triplestore."
if sys.argv[0] != "./"+os.path.basename(__file__):
    print "It must be called as ./"+os.path.basename(__file__)
    sys.exit(0)
    
if len(sys.argv) < 2:
    print "Specify --yes to proceed"
    sys.exit(1)

if sys.argv[1] != "--yes":
    print "Specify --yes to proceed"
    sys.exit(1)

for i in xrange(10):
    print "Destroying everything in %s seconds. Ctrl-C to interrupt the disaster." % (10-i)
    time.sleep(1)

time.sleep(1)
print "Now it's too late."

try:
    print "I can make this triplestore disappear ..."
    store = rdflib.plugin.get('MySQL', store.Store)('rdfstore')
    store.destroy(settings.RDFGRAPH_CONNECT)
    store.open(settings.RDFGRAPH_CONNECT, create=True)
    store.close()
    print "voila' .... it's gone"
    index = indexing.DbIndex()
    index.drop()
    print "and so is the index"
   
except Exception, e:
    print e
    sys.exit(1)

sys.exit(0)
