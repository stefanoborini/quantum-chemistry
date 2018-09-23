import Infoset
import InfosetTypeURI

class InfosetType: 
    def __init__(self, type_uri, dimensionality): # fold>>
        self._type_uri = type_uri
        self._dimensionality = dimensionality
    # <<fold
    def typeURI(self): # fold>>
        return self._type_uri
    # <<fold
    def dimensionality(self): # fold>>
        return self._dimensionality
    # <<fold
    def __cmp__(self, other): # fold>>
        if isinstance(other, InfosetType):
            if cmp(self.dimensionality(), other.dimensionality()) != 0:
                return cmp(self.dimensionality(), other.dimensionality())
            if cmp(self.typeURI(), other.typeURI()) != 0:
                return cmp(self.typeURI(), other.typeURI()) 
            return 0
        return NotImplemented
    # <<fold
    def __hash__(self): # fold>>
        return hash(self.dimensionality()) ^ hash(self.typeURI())

    # <<fold

def getCoordsType(): # fold>>
    return InfosetType(InfosetTypeURI.COORDS_INFOSET_TYPE_URI, 1)
    # <<fold
def getAngleType(): # fold>>
    return InfosetType(InfosetTypeURI.ANGLE_INFOSET_TYPE_URI, 3)
    # <<fold
def getAtomLabelType(): # fold>>
    return InfosetType(InfosetTypeURI.ATOM_LABEL_INFOSET_TYPE_URI, 1)
    # <<fold
def getBondTypeType(): # fold>>
    return InfosetType(InfosetTypeURI.BOND_TYPE_INFOSET_TYPE_URI, 2)
    # <<fold
def getElementType(): # fold>>
    return InfosetType(InfosetTypeURI.ELEMENT_INFOSET_TYPE_URI, 1)
    # <<fold
def getHFEnergyType(): # fold>>
    return InfosetType(InfosetTypeURI.HF_ENERGY_INFOSET_TYPE_URI, 0)
    # <<fold
def getConventionalMoleculeNameType(): # fold>>
    return InfosetType(InfosetTypeURI.CONVENTIONAL_MOLECULE_NAME_TYPE_URI,0)
    # <<fold
def getDaltonOutputFileType(): # fold>>
    return InfosetType(InfosetTypeURI.DALTON_OUTPUT_FILE_INFOSET_TYPE_URI, 0)
    # <<fold
def getFirstHyperpolarizabilityType(components): # fold>>
    return InfosetType(InfosetTypeURI.INFOSET_TYPE_URI_BASE+"FirstHyperpolarizability"+str("".join(components)),0)
    # <<fold
def getSecondHyperpolarizabilityType(components): # fold>>
    return InfosetType(InfosetTypeURI.INFOSET_TYPE_URI_BASE+"SecondHyperpolarizability"+str("".join(components)),0)
    # <<fold
def getMoleculeCodeType(): # fold>>
    return InfosetType(InfosetTypeURI.MOLECULE_CODE_INFOSET_TYPE_URI,0)
    # <<fold 

