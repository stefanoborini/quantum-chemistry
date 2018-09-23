# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
from grrmimport import parsinghelpers
import unittest
import rdflib

class TestDDCAnalysis(unittest.TestCase):
    def testDDCAnalysis(self): 
        graph = rdflib.ConjunctiveGraph()
        p = parsinghelpers.DDCAnalysisParser( graph, os.path.join( os.path.dirname(__file__), "formaldehyde-newnames", "grrm_HCHO_DDC3.log"))
        self.assertEqual(len(p.connectionRouteUris()), 1)
        print graph.serialize()
        
if __name__ == '__main__':
    unittest.main()
    

