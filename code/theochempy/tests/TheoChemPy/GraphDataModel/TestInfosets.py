# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.GraphDataModel import Graph
from theochempy._theochempy.GraphDataModel import Infoset
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy.GraphDataModel import ReificationTypeURI
from theochempy._theochempy import Measure
from theochempy._theochempy import Units
import uuid

class TestInfosets(unittest.TestCase):
    def testInfoset(self): # fold>>
        graph = Graph.Graph()
        node1 = graph.createEntity()
        node2 = graph.createEntity()
        node3 = graph.createEntity()

        coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
        
        self.assertTrue(isinstance(coords, Infoset.Infoset))
        self.assertEqual(coords.graph(), graph)
        self.assertNotEqual(coords.uuid(), None)
        self.assertEqual(coords.typeURI(), InfosetType.getCoordsType().typeURI())
        self.assertEqual(coords.dimensionality(), InfosetType.getCoordsType().dimensionality())
        self.assertEqual(coords.size(), 3)
        self.assertEqual(coords.hasNone(), True)

        

        # <<fold
    def testInfoset2(self): # fold>>
        graph = Graph.Graph()
        coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
        labels = Infoset.Infoset(graph, InfosetType.getAtomLabelType())
        bondtypes = Infoset.Infoset(graph, InfosetType.getBondTypeType())
        angles = Infoset.Infoset(graph, InfosetType.getAngleType())

        node1 = graph.createEntity()
        node2 = graph.createEntity()
        node3 = graph.createEntity()
        link = graph.createEntity((node1,node2))
        angle_entity = graph.createEntity((node1, node2, node3))

        coords.setValue(node1, (10.0,0.0,0.0))
        coords.setValue(node2, (10.0,2.0,0.0))

        self.assertEqual(coords.hasNone(), True)

        coords.setValue(node3, (10.0,2.0,3.0))
        
        self.assertEqual(coords.hasNone(), False)

       
        self.assertEqual(coords.value(node1), (10.0,0.0,0.0))
        self.assertEqual(coords.value(node2), (10.0,2.0,0.0))
        self.assertEqual(coords.value(node3), (10.0,2.0,3.0))

        bondtypes.setValue(link, 2)
        self.assertEqual(bondtypes.value(link), 2)
        self.assertEqual(bondtypes.hasNone(), False)
       
        angles.setValue(angle_entity, Measure.Measure(45.0, Units.degrees))
        self.assertEqual(angles.hasNone(), False)
        self.assertEqual(angles.value(angle_entity).value(), Measure.Measure(45.0, Units.degrees).value())

        graph.deleteEntity(node1)

        self.assertEqual(coords.size(),2)
        self.assertEqual(labels.size(),2)
        self.assertEqual(bondtypes.size(),0)
        self.assertEqual(angles.size(), 0)

        # <<fold
    def testEntityDeletionCascade(self): # fold>>
        graph = Graph.Graph()
        coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
        labels = Infoset.Infoset(graph, InfosetType.getAtomLabelType())
        bondtypes = Infoset.Infoset(graph, InfosetType.getBondTypeType())
        angles = Infoset.Infoset(graph, InfosetType.getAngleType())

        node1 = graph.createEntity()
        node2 = graph.createEntity()
        node3 = graph.createEntity()
        link = graph.createEntity((node1,node2))
        angle_entity = graph.createEntity((node1, node2, node3))

        coords.setValue(node1, (10.0,0.0,0.0))
        coords.setValue(node2, (10.0,2.0,0.0))
        coords.setValue(node3, (10.0,2.0,3.0))

        bondtypes.setValue(link, 2)
        angles.setValue(angle_entity, 45.0)

        graph.deleteEntity(node1)

        self.assertEqual(coords.size(),2)
        self.assertEqual(labels.size(),2)
        self.assertEqual(bondtypes.size(),0)
        self.assertEqual(angles.size(), 0)

        # <<fold
    def testGraphInfoset(self): # fold>>
        graph = Graph.Graph()
        energy = Infoset.Infoset(graph, InfosetType.getHFEnergyType())
        energy.setValue(None, Measure.Measure(10.4, Units.hartree))

        self.assertEqual(energy.dimensionality(),0)
        self.assertEqual(energy.size(),1)

        self.assertEqual(energy.value(None).value(), 10.4)
        self.assertEqual(energy.value(None).unit(), Units.hartree)

        # <<fold
    def testGetInfoset(self): # fold>>
        graph = Graph.Graph()
        coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
        coords2 = Infoset.Infoset(graph, InfosetType.getCoordsType())
        labels = Infoset.Infoset(graph, InfosetType.getAtomLabelType())
        bondtypes = Infoset.Infoset(graph, InfosetType.getBondTypeType())
        angles = Infoset.Infoset(graph, InfosetType.getAngleType())
        energy = Infoset.Infoset(graph, InfosetType.getHFEnergyType())

        self.assertEqual(len(graph.getInfosets()), 6)

        self.assertEqual(len(graph.getInfosets(dimensionality=0)), 1)
        self.assertEqual(len(graph.getInfosets(dimensionality=1)), 3)
        self.assertEqual(len(graph.getInfosets(dimensionality=2)), 1)
        self.assertEqual(len(graph.getInfosets(dimensionality=3)), 1)
        self.assertEqual(len(graph.getInfosets(dimensionality=4)), 0)

        self.assertEqual(len(graph.getInfosets(uuid=coords.uuid())), 1)
        self.assertEqual(len(graph.getInfosets(uuid=labels.uuid())), 1)
        self.assertEqual(len(graph.getInfosets(uuid=uuid.uuid4())), 0)

        self.assertEqual(len(graph.getInfosets(infoset_type=InfosetType.getCoordsType())), 2)
        self.assertEqual(len(graph.getInfosets(infoset_type=InfosetType.getHFEnergyType())), 1)
        self.assertEqual(len(graph.getInfosets(infoset_type=list)), 0)

        self.assertEqual(len(graph.getInfosets(uuid=labels.uuid(), dimensionality=1)), 1)
        self.assertEqual(len(graph.getInfosets(uuid=labels.uuid(), dimensionality=2)), 0)

        # <<fold
    def testReification(self): # fold>>
        graph = Graph.Graph()
        node1 = graph.createEntity()
        node2 = graph.createEntity()
        node3 = graph.createEntity()

        coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
        self.assertEqual(len(coords.getReifications()), 0)

        id = coords.reify(ReificationTypeURI.COMMENT_REIFICATION_TYPE_URI, "hello")
        
        type_uri, value = coords.getReifications(id=id)
        self.assertEqual(type_uri, ReificationTypeURI.COMMENT_REIFICATION_TYPE_URI)
        self.assertEqual(value, "hello")
        self.assertEqual(len(coords.getReifications()), 1)

        
        

        # <<fold

if __name__ == '__main__':
    unittest.main()
    

