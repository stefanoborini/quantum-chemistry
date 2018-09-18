from wavemoldb.ordfm import grrm2

class ConnectionResolver:
    def __init__(self, graph, parsers, mapper):
        self._mapper = mapper
        self._parsers = parsers
        self._graph = graph
        print "Resolving connections"
        for routeinfo in self._mapper.allInterconversionAdditionalInfos():
            start, end = routeinfo.startStructureLabel(), routeinfo.endStructureLabel()
            print "found "+str(start)+" - "+str(end)
            route = routeinfo.interconversion()
            try:
                start_molecule = self._mapper.structureLabelToMolecule(start)
                grrm2.interconversionStart(route).set(start_molecule)
            except KeyError:
                print "Unknown start molecule for interconversion "+str(route)

            try:
                end_molecule = self._mapper.structureLabelToMolecule(end)
                grrm2.interconversionEnd(route).set(end_molecule)
            except KeyError:
                print "Unknown end molecule for interconversion "+str(route)
            
