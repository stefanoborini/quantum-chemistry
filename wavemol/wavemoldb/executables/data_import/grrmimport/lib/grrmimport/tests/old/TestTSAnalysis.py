# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
from grrmimport import parsinghelpers
import unittest
import rdflib
from wavemoldb.ordfm import grrm2

class TestTSAnalysis(unittest.TestCase):
    def testTSAnalysis(self): 
        graph = rdflib.ConjunctiveGraph()
        p = parsinghelpers.TSAnalysisParser( graph, os.path.join( os.path.dirname(__file__), "formaldehyde-newnames", "grrm_HCHO_TS3.log"))
        self.assertEqual(p._forward_route_additional_infos.startStructureLabel(), ("TS", 3))
        self.assertEqual(p._forward_route_additional_infos.endStructureLabel(), ("UDC", 1))
        self.assertEqual(len(grrm2.interconversionStep(p._forward_route).getAll()), 17)
    
        self.assertEqual(p._backward_route_additional_infos.startStructureLabel(), ("TS", 3))
        self.assertEqual(p._backward_route_additional_infos.endStructureLabel(), ("UDC", 2))
        self.assertEqual(len(grrm2.interconversionStep(p._backward_route).getAll()), 19)
        print graph.serialize()
        
if __name__ == '__main__':
    unittest.main()
    

