import simplejson
from . import namespaces
from .. import ThingObject
from .. import DataProperty
from .. import ObjectProperty
from .. import MultipleObjectProperty

import rdflib
import types

# ok guys. here is the deal. I don't want to use seth-scripting for two major reasons:
# first, it interfaces with pellet through jpype, increasing complexity of the runtime
# second, it is basically unmaintained. 
# as I don't have the time to mess with metaclass programming, interface with a reasoner
# etc... and since my ontology is very easy, I am implementing an idiotic mapping with
# dedicated reasoner. I don't want to make history here. I just want to write my damn data,
# and my brain is already at the limit of what I can deal (I have other computational issues
# to solve at the moment).


##########################
# owl datatype properties.

class zeroPointVibrationalEnergy(DataProperty):
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.zeroPointVibrationalEnergy 
    @staticmethod
    def domain():
        return [InterconversionResult]
    @staticmethod
    def range():
        return float
class structureNumber(DataProperty):
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.structureNumber
    @staticmethod
    def domain():
        return [InterconversionResult]
    @staticmethod
    def range():
        return int
class stepNumber(DataProperty):
    @staticmethod
    def domain():
        return [InterconversionStep] 
    @staticmethod
    def range():
        return int
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.stepNumber
class spinMultiplicity(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return int
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.spinMultiplicity
class spin(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return int
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.spin
class smiles(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.smiles
class normalModesEigenvalues(DataProperty):
    def get(self):
        v = super(normalModesEigenvalues,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, eigenvalue_list):
        super(normalModesEigenvalues, self).set(str(simplejson.dumps(eigenvalue_list)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.normalModesEigenvalues
class method(DataProperty):
    @staticmethod
    def domain():
        return [RunData] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.method
class mass(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return float
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.mass
class job(DataProperty):
    @staticmethod
    def domain():
        return [RunData] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.job
class inchi(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.inchi
class hillFormula(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.hillFormula
class geometry(DataProperty):
    def get(self):
        v = super(geometry,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, geometry_data):
        super(geometry, self).set(str(simplejson.dumps(geometry_data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.geometry
class energy(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return float
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.energy
class charge(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return float
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.charge
class basisSet(DataProperty):
    @staticmethod
    def domain():
        return [RunData] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.basisSet

class canostPlanar(DataProperty):
    def get(self):
        v = super(canostPlanar,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        super(canostPlanar, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.canostPlanar
class canostSerial(DataProperty):
    def get(self):
        v = super(canostSerial,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        super(canostSerial, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.canostSerial
class canostSerialCanonical(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.canostSerialCanonical
class canostPlanarCanonical(DataProperty):
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.canostPlanarCanonical
class fragments(DataProperty):
    def get(self):
        v = super(fragments,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        if type(data) != types.ListType:
            raise TypeError("invalid datatype. not a list")
        for d in data:
            if type(d) != types.ListType:
                raise TypeError("invalid datatype. not a list of lists")
            for i in d:
                if type(i) != types.IntType:
                    raise TypeError("invalid datatype. not an int")
        super(fragments, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.fragments
class fragmentsCanostPlanarCanonical(DataProperty):
    def get(self):
        v = super(fragmentsCanostPlanarCanonical,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        if type(data) != types.ListType:
            raise TypeError("not a list")
        for d in data:
            if not type(d) in [types.StringType, types.NoneType]:
                raise TypeError("not a list of strings or None")
        super(fragmentsCanostPlanarCanonical, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.fragmentsCanostPlanarCanonical
class fragmentsCanostSerialCanonical(DataProperty):
    def get(self):
        v = super(fragmentsCanostSerialCanonical,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        if type(data) != types.ListType:
            raise TypeError("not a list")
        for d in data:
            if not type(d) in [types.StringType, types.NoneType]:
                raise TypeError("not a list of strings")
        super(fragmentsCanostSerialCanonical, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.fragmentsCanostSerialCanonical
class fragmentsCanostPlanar(DataProperty):
    def get(self):
        v = super(fragmentsCanostPlanar,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        if type(data) != types.ListType:
            raise TypeError("invalid datatype. not a list")
        for d in data:
            if not type(d) in [types.ListType, types.NoneType]:
                raise TypeError("invalid datatype. not a list of lists or None")
            if type(d) == types.ListType:
                for i in d:
                    if type(i) != types.StringType:
                        raise TypeError("invalid datatype. not a string")
        super(fragmentsCanostPlanar, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.fragmentsCanostPlanar
class fragmentsCanostSerial(DataProperty):
    def get(self):
        v = super(fragmentsCanostSerial,self).get()
        if v:
            return simplejson.loads(v)
        return None
    def set(self, data):
        if type(data) != types.ListType:
            raise TypeError("invalid datatype. not a list")
        for d in data:
            if not type(d) in [types.ListType, types.NoneType]:
                raise TypeError("invalid datatype. not a list of lists")
            if type(d) == types.ListType:
                for i in d:
                    if not type(i) in [types.StringType, types.NoneType]:
                        raise TypeError("invalid datatype. not a string or None")
        super(fragmentsCanostSerial, self).set(str(simplejson.dumps(data)))
    @staticmethod
    def domain():
        return [Molecule] 
    @staticmethod
    def range():
        return str
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.fragmentsCanostSerial

##########################
# owl object properties.

class prevInterconversionStep(ObjectProperty):
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.prevInterconversionStep
    @staticmethod
    def domain():
        return [InterconversionStep]
    @staticmethod
    def range():
        return [InterconversionStep]

class nextInterconversionStep(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def get(self):
        ret = None
        others = self._graph.subjects( predicate=namespaces.GRRM_NS.prevInterconversionStep,object=self._subject)
        for o in others:
            if ret:
                raise Exception("Uniqueness violation in db")
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            ret = tuple(instances)
        return ret 
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.nextInterconversionStep
    @staticmethod
    def domain():
        return [InterconversionStep]
    @staticmethod
    def range():
        return [InterconversionStep]
    
class interconversionStepOf(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def get(self):
        ret = None
        others = self._graph.subjects( predicate=namespaces.GRRM_NS.interconversionStep,object=self._subject)
        for o in others:
            if ret:
                raise Exception("Uniqueness violation in db")
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            ret = tuple(instances)
        return ret 
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.interconversionStepOf
    @staticmethod
    def domain():
        return [InterconversionStep]
    @staticmethod
    def range():
        return [Interconversion]

class interconversionEndOf(object): 
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def getAll(self):
        retlist = None
        others = self._graph.subjects( predicate=namespaces.GRRM_NS.interconversionEnd,object=self._subject)
        for o in others:
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            if retlist is None:
                retlist = []
            retlist.append(tuple(instances))
        return retlist
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.interconversionEndOf
    @staticmethod
    def domain():
        return [InterconversionResult]
    @staticmethod
    def range():
        return [Interconversion]

class interconversionStartOf(object): 
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def getAll(self):
        retlist = None
        others = self._graph.subjects( predicate=namespaces.GRRM_NS.interconversionStart,object=self._subject)
        for o in others:
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            if retlist is None:
                retlist = []
            retlist.append(tuple(instances))
        return retlist
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.interconversionStartOf
    @staticmethod
    def domain():
        return [InterconversionResult]
    @staticmethod
    def range():
        return [Interconversion]

class interconversionStart(ObjectProperty): 
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.interconversionStart
    @staticmethod
    def domain():
        return [Interconversion]
    @staticmethod
    def range():
        return [InterconversionResult]

class interconversionEnd(ObjectProperty): 
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.interconversionEnd
    @staticmethod
    def domain():
        return [Interconversion]
    @staticmethod
    def range():
        return [InterconversionResult]

class runInputOf(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def get(self):
        ret = None
        others = self._graph.subjects( predicate=namespaces.GRRM_NS.runInput,object=self._subject)
        for o in others:
            if ret:
                raise Exception("Uniqueness violation in db")
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            ret = tuple(instances)
        return ret 
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.runInputOf
    @staticmethod
    def domain():
        return [RunInput]
    @staticmethod
    def range():
        return [Run]

class runOutput(MultipleObjectProperty):
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.runOutput
    @staticmethod
    def domain():
        return [Run]
    @staticmethod
    def range():
         return [RunOutput]

class interconversionStep(MultipleObjectProperty):
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.interconversionStep
    @staticmethod
    def domain():
        return [Interconversion]
    @staticmethod
    def range():
         return [InterconversionStep]

class runOutputOf(object):
    def __init__(self, subject):
        self._graph = subject.graph()
        self._subject = rdflib.URIRef(subject.uri())
        try:
            [d.get(self._graph, self._subject) for d in self.domain()]
        except:
            raise Exception("domain violation")
    def get(self):
        ret = None
        others = self._graph.subjects( predicate=namespaces.GRRM_NS.runOutput,object=self._subject)
        for o in others:
            if ret:
                raise Exception("Uniqueness violation in db")
            try:
                instances = [d.get(self._graph, o) for d in self.range()]
            except:
                raise Exception("Invalid graph content: range violated")
            ret = tuple(instances)
        return ret 
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.runOutputOf
    @staticmethod
    def domain():
        return [RunOutput]
    @staticmethod
    def range():
        return [Run]

class runInput(MultipleObjectProperty):
    @staticmethod
    def propertyUri():
        return namespaces.GRRM_NS.runInput
    @staticmethod
    def domain():
        return [Run]
    @staticmethod
    def range():
        return [RunInput]


###############
# owl classes.

# not an owl:thing. A grrm:thing (base class for all our subclasses in this namespace)
# An artifact, if you want, as we don't have a reasoner, I take my chances. 
# Yes, we don't delegate the subclasses set. I don't care (for now). 

class Thing(ThingObject): 
    @staticmethod
    def subclasses():
        return set( [ Run, RunInput, RunOutput, RunData, Molecule, Interconversion, InterconversionStep, InterconversionResult, EquilibriumStructure, TransitionState, BarrierDissociated, BarrierlessDissociated ] ) 
    @staticmethod
    def superclasses():
        return set([])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.Thing

class Run(ThingObject):
    @staticmethod
    def subclasses():
        return set([])
    @staticmethod
    def superclasses():
        return set([Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.Run

class RunInput(ThingObject):
    @staticmethod
    def superclasses():
        return set([Thing])
    @staticmethod
    def subclasses():
        return set( [ RunData, Molecule, InterconversionStep, InterconversionResult, EquilibriumStructure, TransitionState, BarrierDissociated, BarrierlessDissociated ] ) 
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.RunInput

class RunOutput(ThingObject):
    @staticmethod
    def superclasses():
        return set([Thing])
    @staticmethod
    def subclasses():
        return set( [ Interconversion, Molecule, InterconversionStep, InterconversionResult, EquilibriumStructure, TransitionState, BarrierDissociated, BarrierlessDissociated ] ) 
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.RunOutput
        
class Interconversion(ThingObject):
    @staticmethod
    def superclasses():
        return set([Thing, RunOutput])
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.Interconversion
   
class Molecule(ThingObject): 
    @staticmethod
    def subclasses():
        return set([ InterconversionStep, InterconversionResult, EquilibriumStructure, TransitionState, BarrierDissociated, BarrierlessDissociated]) 
    @staticmethod
    def superclasses():
        return set([RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.Molecule

class RunData(ThingObject):
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def superclasses():
        return set([RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.RunData

class InterconversionStep(ThingObject):
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def superclasses():
        return set([Molecule, RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.InterconversionStep
    
class InterconversionResult(ThingObject):
    @staticmethod
    def subclasses():
        return set([ EquilibriumStructure, TransitionState, BarrierDissociated, BarrierlessDissociated]) 
    @staticmethod
    def superclasses():
        return set([Molecule, RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.InterconversionResult

class EquilibriumStructure(ThingObject):
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def superclasses():
        return set([InterconversionResult, Molecule, RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.EquilibriumStructure
    def uri(self):
        return self._uri

class TransitionState(ThingObject):
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def superclasses():
        return set([InterconversionResult, Molecule, RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.TransitionState

class BarrierDissociated(ThingObject):
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def superclasses():
        return set([InterconversionResult, Molecule, RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.BarrierDissociated

class BarrierlessDissociated(ThingObject):
    @staticmethod
    def subclasses():
        return set([]) 
    @staticmethod
    def superclasses():
        return set([InterconversionResult, Molecule, RunOutput, RunInput, Thing])
    @staticmethod
    def typeUri():
        return namespaces.GRRM_NS.BarrierlessDissociated
