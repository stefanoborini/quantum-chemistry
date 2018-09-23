# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest
import time
import shutil

from theochempy._theochempy.Databases.Simple import DBAccess

from theochempy._theochempy.GraphDataModel import Graph
from theochempy._theochempy.GraphDataModel import Infoset
from theochempy._theochempy.GraphDataModel import InfosetType

from theochempy._theochempy import Measure
from theochempy._theochempy import Units

def moduleDir():
    return os.path.dirname(__file__)

class TestDBAccess(unittest.TestCase):
    def testDBAccessInit(self): # fold>>
        try:
            os.unlink(os.path.join(moduleDir(), "testdb"))
        except:
            pass
        DBAccess.init(os.path.join(moduleDir(), "testdb"))

        self.assertTrue(os.path.exists(os.path.join(moduleDir(), "testdb", ".meta")))
        self.assertTrue(os.path.exists(os.path.join(moduleDir(), "testdb", ".meta","version")))
        # <<fold
    
    def testStoreAndRetrieve(self):
        reinitdb() 
        graph = Graph.Graph()
        coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
        labels = Infoset.Infoset(graph, InfosetType.getAtomLabelType())
        bondtypes = Infoset.Infoset(graph, InfosetType.getBondTypeType())
        energy = Infoset.Infoset(graph, InfosetType.getHFEnergyType())
        angles = Infoset.Infoset(graph, InfosetType.getAngleType())

        node1 = graph.createEntity()
        node2 = graph.createEntity()
        node3 = graph.createEntity()
        link = graph.createEntity((node1,node2))
        angle = graph.createEntity((node1,node2, node3))

        coords.setValue(node1, (10.0,0.0,0.0))
        coords.setValue(node2, (10.0,2.0,0.0))
        coords.setValue(node3, (10.0,2.0,3.0))
       
        bondtypes.setValue(link, 2)
        angles.setValue(angle, Measure.Measure(45, Units.degrees))

        db = DBAccess.DBAccess(os.path.join(moduleDir(), "testdb"))
        db.store(graph)
        

        molecule_list = db.retrieveAll()
        self.assertEqual(len(molecule_list), 1)

    def testMetainfo(self):
        reinitdb() 
        db = DBAccess.DBAccess(os.path.join(moduleDir(), "testdb"))
        db.setMetainfo("integer", 123)
       
        value = db.metainfo("integer")
        self.assertEqual(value, 123)

        db.setMetainfo("tuple", (1,2,3))
       
        value = db.metainfo("tuple")
        self.assertEqual(value, (1,2,3))

        db.setMetainfo("string", "hello")
       
        value = db.metainfo("string")
        self.assertEqual(value, "hello")

        value = db.metainfo("unexistent")
        self.assertEqual(value, None)

        
    def testSearch(self):
        reinitdb()
        db = DBAccess.DBAccess(os.path.join(moduleDir(), "testdb"))
        
        for i in xrange(1,90):
            graph=Graph.Graph()
            coords = Infoset.Infoset(graph, InfosetType.getCoordsType())
            labels = Infoset.Infoset(graph, InfosetType.getAtomLabelType())
            bondtypes = Infoset.Infoset(graph, InfosetType.getBondTypeType())
            energy = Infoset.Infoset(graph, InfosetType.getHFEnergyType())
            angles = Infoset.Infoset(graph, InfosetType.getAngleType())

            node1 = graph.createEntity()
            node2 = graph.createEntity()
            node3 = graph.createEntity()
            link = graph.createEntity((node1,node2))
            angle = graph.createEntity((node1,node2, node3))
    
            coords.setValue(node1, (10.0,0.0,0.0))
            coords.setValue(node2, (10.0,2.0,0.0))
            coords.setValue(node3, (10.0,2.0,3.0))
        
            bondtypes.setValue(link, 2)
    
            angles.setValue(angle, Measure.Measure(float(i), Units.degrees))
            db.store(graph)

        class Search:
            def __init__(self, angle):
                self._angle = angle
            def satisfiedBy(self, graph):
                infoset = graph.getInfosets(infoset_type=InfosetType.getAngleType())[0]
                if infoset is None:
                    return False
                #if infoset.value(angle).value() > 45.0 and infoset.value(angle).value() < 48.0:
                #    return True
                if infoset.value(angle).value() % 2 == 0:
                    return True

                return False

        results = db.search(Search(angle))
        #self.assertEqual(len(results), 2)
        for i in results:
            print i.getInfosets(infoset_type=InfosetType.getAngleType())[0].value(angle)


def reinitdb():
    try:
        shutil.rmtree(os.path.join(moduleDir(), "testdb"))
    except Exception, e:
        print e
    DBAccess.init(os.path.join(moduleDir(), "testdb"))


if __name__ == '__main__':
    unittest.main()
    

