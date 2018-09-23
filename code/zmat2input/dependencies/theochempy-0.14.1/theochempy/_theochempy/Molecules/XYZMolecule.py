from theochempy._theochempy import Units 
from theochempy._theochempy import Measure
from theochempy._theochempy.Math import Quaternion
from theochempy._theochempy.GraphDataModel import Graph
from theochempy._theochempy.GraphDataModel import Infoset
from theochempy._theochempy.GraphDataModel import InfosetType

import numpy

class XYZMolecule:
    def __init__(self, atom_list): # fold>>
        self._graph = Graph.Graph()
        self._elements = Infoset.Infoset(self._graph, InfosetType.getElementType())
        self._labels = Infoset.Infoset(self._graph, InfosetType.getAtomLabelType())
        self._coords = Infoset.Infoset(self._graph, InfosetType.getCoordsType())

        for atom in atom_list:
            entity = self._graph.createEntity()
            self._elements.setValue(entity, atom[0])
            self._coords.setValue(entity, atom[1])
        # <<fold
    def elements(self): # fold>>
        return [x[1] for x in self._elements.allValues()]
        # <<fold
    def atomPos(self): # fold>>
        return [x[1] for x in self._coords.allValues()]
        # <<fold
        
    def translate(self, vector): # fold>>
        for entity, pos in self._coords.allValues():
            if pos.unit() == vector.unit():
                newpos = Measure.Measure( (pos.value()[0]+vector.value()[0], pos.value()[1]+vector.value()[1], pos.value()[2]+vector.value()[2]), pos.unit())
            else:
                x_conv = vector.value()[0]*vector.unit().as(pos.unit())
                y_conv = vector.value()[1]*vector.unit().as(pos.unit())
                z_conv = vector.value()[2]*vector.unit().as(pos.unit())
                newpos = Measure.Measure( (pos.value()[0]+x_conv.asNumber(), pos.value()[1]+y_conv.asNumber(), pos.value()[2]+z_conv.asNumber()), pos.unit())
            self._coords.setValue(entity, newpos)
    
    # <<fold
    def rotate(self, axis, angle): # fold>>
        atom_list = []
        q = Quaternion(axis, angle)
        m = q.toRotationMatrix()
        for entity, pos in self._coords.allValues():
            arr = numpy.array([ pos.value()[0], pos.value()[1], pos.value()[2], 1.0 ])
            rotated = numpy.dot(m, arr)
            newpos = Measure.Measure( (rotated[0], rotated[1], rotated[2]), pos.unit())

            self._coords.setValue(entity, newpos)
    # <<fold
        
def centerOfMass(molecule): # fold>>
    numpy.array([0.0, 0.0, 0.0])

    total_mass = 0.0
    center_of_mass = numpy.array([0.0,0.0,0.0])
    for element, coordinate in zip(molecule.elements(), molecule.atomPos()):
        mass_dalton = element.mass().asUnit(Units.dalton).value()
        coordinate_bohr = coordinate.asUnit(Units.bohr).value()

        center_of_mass[0] = center_of_mass[0]+coordinate_bohr[0]*mass_dalton
        center_of_mass[1] = center_of_mass[1]+coordinate_bohr[1]*mass_dalton
        center_of_mass[2] = center_of_mass[2]+coordinate_bohr[2]*mass_dalton

        total_mass += mass_dalton
    
    return Measure.Measure(center_of_mass/total_mass, Units.bohr)
    # <<fold

def momentsOfInertia(molecule, origin_to_center_of_mass=True): # fold>>
    tensor = numpy.zeros((3,3))

    center_of_mass = centerOfMass(molecule)

    for element, coordinate in zip(molecule.elements(), molecule.atomPos()):
        mass_dalton = element.mass().asUnit(Units.dalton).value()

        coordinate_bohr = coordinate.asUnit(Units.bohr).value()
        x = coordinate_bohr[0] - center_of_mass.asUnit(Units.bohr).value()[0]
        y = coordinate_bohr[1] - center_of_mass.asUnit(Units.bohr).value()[1]
        z = coordinate_bohr[2] - center_of_mass.asUnit(Units.bohr).value()[2]

        tensor[0,0] += mass_dalton * (y**2 + z**2)
        tensor[0,1] -= mass_dalton * x * y
        tensor[0,2] -= mass_dalton * x * z
        tensor[1,1] += mass_dalton * (x**2 + z**2)
        tensor[1,2] -= mass_dalton * y * z
        tensor[2,2] += mass_dalton * (x**2 + y**2)


    # symmetrize
    tensor[1,0] = tensor[0,1]
    tensor[2,0] = tensor[0,2]
    tensor[2,1] = tensor[1,2]

    val,vec = numpy.linalg.eig(tensor)

    inertia = []
    for i in xrange(0,3):
        axis = Measure.Measure( (vec[0][i], vec[1][i], vec[2][i]), Units.bohr)
        moment = Measure.Measure(val[i], Units.dalton * Units.bohr * Units.bohr)
        inertia.append( (moment, axis) ) 

    return sorted(inertia, key=lambda x: x[0].value())
# <<fold

