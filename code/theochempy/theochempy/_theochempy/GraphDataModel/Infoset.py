import uuid
import types

class Infoset(object):
    def __init__(self, graph, infoset_type): # fold>>
        self._graph = graph
        self._infoset_type = infoset_type
        self._uuid = uuid.uuid4()
        self._data = {}
        self._reifications = {}
        self._graph._registerInfoset(self)

    # <<fold
    def graph(self): # fold>>
        return self._graph
    # <<fold
    def uuid(self): # fold>>
        return self._uuid
    # <<fold
    def typeURI(self): # fold>>
        return self._infoset_type.typeURI()
    # <<fold
    def dimensionality(self): # fold>>
        return self._infoset_type.dimensionality()
    # <<fold
    def type(self): # fold>>
        return self._infoset_type
    # <<fold
    def size(self): # fold>>
        return len(self._data)
    # <<fold
    def hasNone(self): # fold>>
        return None in self._data.values()
    # <<fold
    def value(self, entity): # fold>>
        if type(entity) == types.TupleType:
            if len(entity) != self._infoset_type.dimensionality():
                raise ValueException("Invalid length for entity")
            return self._data[entity]
        elif self._infoset_type.dimensionality() == 0:
            return self._data[self._graph]
        else:
            return self._data[entity]
    # <<fold
    def setValue(self, entity, value): # fold>>
            
        if type(entity) == types.TupleType:
            if len(entity) != self._infoset_type.dimensionality():
                raise ValueException("Invalid length for entity")
            self._data[tuple(entity)] = value
        elif self._infoset_type.dimensionality() == 0:
            self._data[self._graph] = value
        else:
            self._data[entity] = value
    # <<fold

    def _addSpace(self, entity): # fold>>
        self._data[entity]=None
    # <<fold
    def _removeSpace(self, entity): # fold>>
        del self._data[entity]
    # <<fold

    def allValues(self): # fold>>
        return self._data.items()
    # <<fold
    def reify(self, type_uri, value): # fold>>
        reification_uuid = uuid.uuid4()
        self._reifications[reification_uuid] = (type_uri, value)
        return reification_uuid
    # <<fold 
    def getReifications(self, id=None): # fold>>
        if id is not None:
            if self._reifications.has_key(id):
                return self._reifications[id]
            return None
        else:
            return self._reifications.values()
    # <<fold

