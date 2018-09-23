from wavemol.core import units
import simplejson

# helper functions
def parseGeometryToken(token): # fold>>
    geometry = {}
    geometry["labels"] = []
    geometry["symbols"] = []
    geometry["coordinates"] = []

    for symbol, coords in token.atomList():
        coords.units = units.angstrom
        geometry["labels"].append( symbol )
        geometry["symbols"].append( symbol )
        geometry["coordinates"].append(list(coords.magnitude))

    return geometry
def parseEnergyToken(token): # fold>>
    energy = token.energy()
    energy.units = units.hartree
    return float(energy.magnitude)
def parseZPVEToken(token): # fold>>
    zpve = token.zpve()
    zpve.units = units.hartree
    return float(zpve.magnitude)
def parseNormalModesEigenvalues(token): # fold>>
    def _convert(value):
        value.units = units.hartree
        return float(value.magnitude)

    eig = token.eigenvalues()
    return map(_convert, eig)


