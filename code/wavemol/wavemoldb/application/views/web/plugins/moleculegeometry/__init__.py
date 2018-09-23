from lib import filestorage
from application.views.web import plugins
from application import graphstore

from wavemoldb.ordfm import grrm2

import settings

class RequestHandler(object):
    def __init__(self):
        pass

    def dispatch(self, request, uri):
        context = {}
        graph = graphstore.graph()

        try:
            molecule = grrm2.Molecule.get(graph, uri)
        except:
            molecule = None

        if not molecule:
            return None

        fs = filestorage.ResourceStorage(molecule, web_accessible=True, settings=settings.filestorage_settings)
        context["xyzFilePath"] = fs.url("geometry","xyz")
        if not fs.readable("geometry","xyz"):
            context = None
            
        return context




class MoleculeGeometryPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(MoleculeGeometryPlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "moleculegeometry"
    def visibleName(self):
        return "Geometry"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return MoleculeGeometryPlugin()
