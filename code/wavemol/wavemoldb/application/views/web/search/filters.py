import warnings
from lib import utils
import md5
import base64

_filter_list=None
def _registerFilter(filter):
    global _filter_list
    if _filter_list is None:
        _filter_list = {}

    _filter_list[filter.typeId()] = filter

def fromTypeId(type_id):
    return _filter_list.get(type_id, None)

# add new filters here

class GrrmTypeFilter(object):
    def __init__(self,grrm_type):
        super(GrrmTypeFilter, self).__init__()
        if grrm_type not in ( "grrm__equilibrium_structure", "grrm__transition_state", "grrm__barrierless_dissociated", "grrm__barrier_dissociated", "grrm__run", "grrm__interconversion_step", "grrm__interconversion", "grrm__molecule"):
            raise Exception("invalid type for GrrmTypeFilter")
        self._grrm_type = str(grrm_type)
    @classmethod
    def typeId(cls):
        return "grrm__type"
    def apply(self, query):
        if self._grrm_type == "grrm__equilibrium_structure":
            query.filter("is_grrm__equilibrium_structure = True") 
        elif self._grrm_type == "grrm__transition_state":
            query.filter("is_grrm__transition_state = True") 
        elif self._grrm_type == "grrm__barrierless_dissociated":
            query.filter("is_grrm__barrierless_dissociated= True") 
        elif self._grrm_type == "grrm__barrier_dissociated":
            query.filter("is_grrm__barrier_dissociated= True") 
        elif self._grrm_type == "grrm__run":
            query.filter("is_grrm__run= True") 
        elif self._grrm_type == "grrm__interconversion_step":
            query.filter("is_grrm__interconversion_step=True") 
        elif self._grrm_type == "grrm__interconversion":
            query.filter("is_grrm__interconversion=True") 
        elif self._grrm_type == "grrm__molecule":
            query.filter("is_grrm__molecule=True") 
        return query
_registerFilter(GrrmTypeFilter)

class GrrmEnergyBetweenFilter(object):
    def __init__(self,low,high):
        super(GrrmEnergyBetweenFilter, self).__init__()
        try:
            self._low = float(low)
            self._high = float(high)
        except:
            raise Exception("Invalid values for floating point energy values")
    @classmethod
    def typeId(cls):
        return "grrm__energy_between"
    def apply(self, query):
        query.filter("(grrm__energy >= "+str(self._low)+" AND grrm__energy <= "+str(self._high)+")")
        return query
_registerFilter(GrrmEnergyBetweenFilter)

class GrrmCarbonsBetweenFilter(object):
    def __init__(self,low,high):
        super(GrrmCarbonsBetweenFilter, self).__init__()
        try:
            self._low = int(low)
            self._high = int(high)
        except:
            raise Exception("Invalid values for integer number of carbons values")
    @classmethod
    def typeId(cls):
        return "grrm__carbons_between"
    def apply(self, query):
        query.filter("(grrm__carbons >= "+str(self._low)+" AND grrm__carbons <= "+str(self._high)+")")
        return query
_registerFilter(GrrmCarbonsBetweenFilter)

class GrrmHydrogensBetweenFilter(object):
    def __init__(self,low,high):
        super(GrrmHydrogensBetweenFilter, self).__init__()
        try:
            self._low = int(low)
            self._high = int(high)
        except:
            raise Exception("Invalid values for integer number of hydrogens values")
    @classmethod
    def typeId(cls):
        return "grrm__hydrogens_between"
    def apply(self, query):
        query.filter("(grrm__hydrogens >= "+str(self._low)+" AND grrm__hydrogens <= "+str(self._high)+")")
        return query
_registerFilter(GrrmHydrogensBetweenFilter)

class GrrmNitrogensBetweenFilter(object):
    def __init__(self,low,high):
        super(GrrmNitrogensBetweenFilter, self).__init__()
        try:
            self._low = int(low)
            self._high = int(high)
        except:
            raise Exception("Invalid values for integer number of nitrogens values")
    @classmethod
    def typeId(cls):
        return "grrm__nitrogens_between"
    def apply(self, query):
        query.filter("(grrm__nitrogens >= "+str(self._low)+" AND grrm__nitrogens <= "+str(self._high)+")")
        return query
_registerFilter(GrrmNitrogensBetweenFilter)

class GrrmOxygensBetweenFilter(object):
    def __init__(self,low,high):
        super(GrrmOxygensBetweenFilter, self).__init__()
        try:
            self._low = int(low)
            self._high = int(high)
        except:
            raise Exception("Invalid values for integer number of oxygensvalues")
    @classmethod
    def typeId(cls):
        return "grrm__oxygens_between"
    def apply(self, query):
        query.filter("(grrm__oxygens >= "+str(self._low)+" AND grrm__oxygens <= "+str(self._high)+")")
        return query
_registerFilter(GrrmOxygensBetweenFilter)

class GrrmSmilesFilter(object):
    def __init__(self,smiles):
        super(GrrmSmilesFilter, self).__init__()
        try:
            self._smiles = base64.b32decode(str(smiles).strip())
        except:
            raise Exception("Invalid values for smiles")
    @classmethod
    def typeId(cls):
        return "grrm__smiles"
    def apply(self, query):
        query.filter("grrm__smiles_md5 = '"+str(md5.md5(self._smiles).hexdigest())+"'")
        return query
_registerFilter(GrrmSmilesFilter)

class GrrmInchiFilter(object):
    def __init__(self,inchi):
        super(GrrmInchiFilter, self).__init__()
        try:
            self._inchi = base64.b32decode(str(inchi).strip())
        except:
            raise Exception("Invalid values for inchi")
    @classmethod
    def typeId(cls):
        return "grrm__inchi"
    def apply(self, query):
        query.filter("grrm__inchi_md5 = '"+str(md5.md5(self._inchi).hexdigest())+"'")
        return query
_registerFilter(GrrmInchiFilter)

class GrrmCanostPlanarFilter(object):
    def __init__(self,canost_planar):
        super(GrrmCanostPlanarFilter, self).__init__()
        try:
            self._canost_planar = base64.b32decode(str(canost_planar).strip())
        except:
            raise Exception("Invalid values for canost_planar")
    @classmethod
    def typeId(cls):
        return "grrm__canost_planar"
    def apply(self, query):
        query.filter("grrm__canost_planar_md5 = '"+str(md5.md5(self._canost_planar).hexdigest())+"'")
        print self._canost_planar, str(md5.md5(self._canost_planar).hexdigest())
        return query
_registerFilter(GrrmCanostPlanarFilter)

class GrrmMassBetweenFilter(object):
    def __init__(self,low,high):
        super(GrrmMassBetweenFilter, self).__init__()
        try:
            self._low = float(low)
            self._high = float(high)
        except:
            raise Exception("Invalid values for floating point mass values")
    @classmethod
    def typeId(cls):
        return "grrm__mass_between"
    def apply(self, query):
        query.filter("(grrm__mass >= "+str(self._low)+" AND grrm__mass <= "+str(self._high)+")")
        return query
_registerFilter(GrrmMassBetweenFilter)

class GrrmBasisSetFilter(object):
    def __init__(self,basis_set):
        super(GrrmBasisSetFilter, self).__init__()
        try:
            self._basis_set = str(basis_set)
        except:
            raise Exception("Invalid value for basis_set")
    @classmethod
    def typeId(cls):
        return "grrm__basis_set"
    def apply(self, query):
        query.filter("(grrm__basis_set = '"+str(self._basis_set)+"')")
        return query
_registerFilter(GrrmBasisSetFilter)
