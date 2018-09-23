# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.GraphDataModel import Graph

class TestGraph(unittest.TestCase):
    def testGraph(self): # fold>>
        graph = Graph.Graph()

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        node1 = graph.createEntity()

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        node2 = graph.createEntity()

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 2)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        node3 = graph.createEntity()

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 3)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        node4 = graph.createEntity()

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 4)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        link1 = graph.createEntity(entities=(node1, node2))

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 4)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        surface1 = graph.createEntity(entities=(node1, node2, node3))

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 4)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        hypersurface1 = graph.createEntity(entities=(node1, node2, node3, node4))

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 4)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 1)
        # <<fold
    def testRemoval(self): # fold>>
        graph = Graph.Graph()

        node1 = graph.createEntity()
        node2 = graph.createEntity()
        node3 = graph.createEntity()
        node4 = graph.createEntity()
        link1 = graph.createEntity(entities=(node1, node2))
        surface1 = graph.createEntity(entities=(node1, node2, node3))
        hypersurface1 = graph.createEntity(entities=(node1, node2, node3, node4))

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 4)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 1)
        
        graph.deleteEntity(node4)

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 3)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        graph.deleteEntity(node1)

        self.assertEqual(len(graph.entityList(dimensionality=0)), 1)
        self.assertEqual(len(graph.entityList(dimensionality=1)), 2)
        self.assertEqual(len(graph.entityList(dimensionality=2)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=3)), 0)
        self.assertEqual(len(graph.entityList(dimensionality=4)), 0)

        # <<fold

if __name__ == '__main__':
    unittest.main()
    

