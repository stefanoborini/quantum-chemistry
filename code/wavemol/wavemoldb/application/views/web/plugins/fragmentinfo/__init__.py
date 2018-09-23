from lib import utils
from lib import chemistry
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
            return None

        if grrm2.fragments(molecule).get() is None:
            return None

        context["fragmentInfo"] = []
        fragments = grrm2.fragments(molecule).get()
        geometry = grrm2.geometry(molecule).get()
        canost_planar = grrm2.fragmentsCanostPlanar(molecule).get()
        canost_serial = grrm2.fragmentsCanostSerial(molecule).get()
        canost_planar_canonical = grrm2.fragmentsCanostPlanarCanonical(molecule).get()
        canost_serial_canonical = grrm2.fragmentsCanostSerialCanonical(molecule).get()

        for i, frag in enumerate(fragments):
            fragment_info = {}
            fragment_info["index"] = i
            fragment_info["atomIndices"] = str(frag)
            symbols = [geometry["symbols"][j-1] for j in frag] 
            fragment_info["hillFormula"] = str(chemistry.hillFormula(symbols))
            try:
                fragment_info["canostPlanar"] = "|".join(canost_planar[i])
            except:
                fragment_info["canostPlanar"] = None

            try:
                fragment_info["canostSerial"] = "|".join(canost_serial[i])
            except:
                fragment_info["canostSerial"] = None

            try:
                fragment_info["canostPlanarCanonical"] = canost_planar_canonical[i]
            except:
                fragment_info["canostPlanarCanonical"] = None
                
            try:
                fragment_info["canostSerialCanonical"] = canost_serial_canonical[i]
            except:
                fragment_info["canostSerialCanonical"] = None


            context["fragmentInfo"].append(fragment_info)

        return context

class FragmentInfoPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(FragmentInfoPlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "fragmentinfo"
    def visibleName(self):
        return "Fragments Information"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return FragmentInfoPlugin()
