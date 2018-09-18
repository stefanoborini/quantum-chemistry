# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
from grrmimport import parsinghelpers
import unittest
import rdflib

class TestOutputDDCFileParser(unittest.TestCase):
    def testParser(self): 
        graph = rdflib.ConjunctiveGraph()
        p = parsinghelpers.OutputDDCFileParser( graph, os.path.join( os.path.dirname(__file__), "formaldehyde-newnames", "grrm_HCHO_DDC_list.log"))
        self.assertEqual(len(p.moleculeUris()), 6)
        print graph.serialize()
        
if __name__ == '__main__':
    unittest.main()
    

