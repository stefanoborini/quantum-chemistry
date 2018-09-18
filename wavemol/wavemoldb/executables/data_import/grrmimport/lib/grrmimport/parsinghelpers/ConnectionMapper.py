class ConnectionMapper:
    def __init__(self, all_connections, structure_label_to_molecule_mapper, all_interconversion_additional_infos):
        self._all_connections = all_connections
        self._structure_label_to_molecule_mapper = structure_label_to_molecule_mapper
        self._all_interconversion_additional_infos = all_interconversion_additional_infos

    def structureLabelToMolecule(self, structure_label):
        return self._structure_label_to_molecule_mapper[structure_label]

    def allInterconversionAdditionalInfos(self):
        return self._all_interconversion_additional_infos


    # FIXME remove
    def allConnectionsFor(self, structure_label):
        all_connections_for = []

        for first, second in self._all_connections:
            if first == structure_label:
                all_connections_for.append(second)
            elif second == structure_label:
                all_connections_for.append(first)
        return set(all_connections_for)

    #FIXME remove
    def allStructureLabels(self):
        tot = []
        for i in self._all_connections:
            tot.extend(list(i))
        return set(tot)

    # FIXME remove
    def interconversionFor(self, structure_label_1, structure_label_2):
        routes = []
        for routeinfo in self._all_interconversion_additional_infos:
            if (routeinfo.startStructureLabel() == structure_label_1 and routeinfo.endStructureLabel() == structure_label_2) or \
                (routeinfo.startStructureLabel() == structure_label_2 and routeinfo.endStructureLabel() == structure_label_1):
                routes.append(routeinfo.interconversion())

        if len(routes) > 1:
            raise Exception("Multiple ("+str(len(routes))+") routes from "+str(structure_label_1)+" to "+str(structure_label_2))
        return routes[0]
