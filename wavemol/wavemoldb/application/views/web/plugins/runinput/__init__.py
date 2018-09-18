from application.views.web import plugins
from lib import utils
from wavemoldb.ordfm import grrm2
from application import graphstore


class RequestHandler(object):
    def __init__(self):
        pass

    def dispatch(self, request, **args):
        graph = graphstore.graph()
        try:
            run = grrm2.Run.get(graph, args["uri"])
        except:
            return None

        return_dict = { "input" : [], 
                        "output": [], 
                      }

        for input_tuple in grrm2.runInput(run).getAll():
            resource = input_tuple[0]

            input = {}
            return_dict["input"].append(input)
            input["uuid"] = utils.uriToUuid(resource.uri())
            input["data"] = {}

            run_data = grrm2.RunData.tryCast(resource)
            if run_data:
                input["data"]["Type"] = "RunData"
                input["data"]["Basis set"] = grrm2.basisSet(run_data).get()
                input["data"]["Method"] = grrm2.method(run_data).get()
                input["data"]["Job"] = grrm2.job(run_data).get()
                continue

            molecule= grrm2.Molecule.tryCast(resource)
            if molecule:
                input["url"] = "/resources/%7B"+input["uuid"]+"%7D"
                input["data"]["Type"] = "Molecule"
                input["data"]["Hill Formula"] = grrm2.hillFormula(molecule).get()
                input["data"]["Mass"] = grrm2.mass(molecule).get()
                input["data"]["SMILES"] = grrm2.smiles(molecule).get()
                input["data"]["InChi"] = grrm2.inchi(molecule).get()
                input["data"]["Spin Multiplicity"] = grrm2.spinMultiplicity(molecule).get()
                continue

            input["data"]["Type"] = "Unknown"

        return return_dict


class RunInputPlugin(plugins.AbstractPlugin):
    def __init__(self):
        super(RunInputPlugin, self).__init__()
        self._request_handler = None
    def name(self):
        return "runinput"
    def visibleName(self):
        return "Input"
    def requestHandler(self):
        if self._request_handler == None:
            self._request_handler = RequestHandler()
        return self._request_handler

def init():
    return RunInputPlugin()

