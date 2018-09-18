import rdflib
import settings
from wavemoldb.ordfm import contexts
_store = None

def store():
    global _store

    if _store:
        return _store

    _store = rdflib.plugin.get('MySQL', rdflib.store.Store)('rdfstore')

    rt = _store.open(settings.RDFGRAPH_CONNECT)
    if rt != rdflib.store.VALID_STORE:
        raise Exception("Invalid store")

    return _store

def graph():

    s = store()
    graph = rdflib.ConjunctiveGraph(s, identifier = contexts.CONTEXT_NS.Default)

    return graph


