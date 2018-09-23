#/usr/bin/env python
# @author Stefano Borini

import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])
    print ""
    print "Initializes the rdf database. Will not destroy it if already present"
    print ""
    if error is not None:
        print ""
        printout.error(error)
        print ""

import rdflib
import settings

store = rdflib.plugin.get('MySQL', rdflib.store.Store)('rdfstore')

print "Trying to create rdf graph storage"
print settings.RDFGRAPH_CONNECT

rt = store.open(settings.RDFGRAPH_CONNECT, create=False)
if rt == rdflib.store.VALID_STORE:
    print "Already exists. no problem. Exiting."
else:
    store.open(settings.RDFGRAPH_CONNECT, create=True)
    store.close()
    rt = store.open(settings.RDFGRAPH_CONNECT, create=False)
    if rt == rdflib.store.VALID_STORE:
        print "Store successfully created"
    else:
        print "WARNING: Unsuccessful in creating store"
        sys.exit(1)

sys.exit(0)
