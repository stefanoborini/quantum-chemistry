import types
import itertools
import uuid

class Graph:
    def __init__(self): # fold>>
        self._entities = { 0: [ self ], 1 : [] }
        self._infosets = { 0: [], 1: []}
        self._oid = 1
        self._uuid = uuid.uuid4()
        # <<fold 
    def entityList(self, dimensionality): # fold>>
        if self._entities.has_key(dimensionality):
            return self._entities[dimensionality]
        return []
        # <<fold
    def createEntity(self, entities=None): # fold>>
        if entities is None:
            id = self._oid
            self._entities[1].append(id)
            for infoset in self._infosets[1]:
                infoset._addSpace(id)
            self._oid += 1
            return id
        
        dimensionality = len(entities)
        if not self._entities.has_key(dimensionality):
            self._entities[dimensionality] = []

        self._entities[dimensionality].append(entities)

        # sync infosets
        if not self._infosets.has_key(dimensionality):
            self._infosets[dimensionality] = []

        for infoset in self._infosets[dimensionality]:
            infoset._addSpace(entities)

        return entities
        # <<fold
    def deleteEntity(self, entity): # fold>>
        if type(entity) == types.TupleType:
            dimensionality = len(entity)
            self._entities[dimensionality].remove(entity)
            for infoset in self._infosets[dimensionality]:
                infoset._removeSpace(entity)
        else:
            self._entities[1].remove(entity)
            for infoset in self._infosets[1]:
                infoset._removeSpace(entity)

            for k,l in self._entities.items():
                if k == 0 or k == 1: continue
                for e in l:
                    if entity in e:
                        l.remove(e)
                        if self._infosets.has_key(len(e)):
                            for infoset in self._infosets[len(e)]:
                                try:
                                    infoset._removeSpace(e)
                                except:
                                    pass
        # <<fold
    def getInfosets(self, dimensionality=None, infoset_type=None, uuid=None): # fold>>
        infosets = None
        if dimensionality is not None:
            if not self._infosets.has_key(dimensionality):
                return []
            infosets = self._infosets[dimensionality]
        else:
            infosets = list( itertools.chain(*self._infosets.values())) # all of them

        if infoset_type is not None:
            infosets = filter(lambda x: x.type() == infoset_type, infosets)

        if uuid is not None:
            infosets = filter(lambda x: x.uuid() == uuid, infosets)

        return infosets
        # <<fold
    def uuid(self): # fold>>
        return self._uuid 
    # <<fold
    def _registerInfoset(self, infoset): # fold>>
        dimensionality = infoset.dimensionality()
        if not self._infosets.has_key(dimensionality):
            self._infosets[dimensionality] = []
        self._infosets[dimensionality].append(infoset)

        if not self._entities.has_key(dimensionality):
            self._entities[dimensionality] = []
        for entity in self._entities[dimensionality]:
            infoset._addSpace(entity)
        # <<fold
