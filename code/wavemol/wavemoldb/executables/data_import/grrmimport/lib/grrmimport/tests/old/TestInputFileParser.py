# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
from grrmimport import parsinghelpers
import unittest
import rdflib
from wavemoldb.ordfm import grrm2

class TestInputParser(unittest.TestCase):
    def testInputParser(self): 
        graph = rdflib.ConjunctiveGraph()
        p = parsinghelpers.InputFileParser(graph, os.path.join( os.path.dirname(__file__), "formaldehyde-newnames", "grrm_HCHO.com"))
        self.assertNotEqual(p.runUri(), None)
        run = grrm2.Run.get(graph, p.runUri())
        self.assertEqual(len(grrm2.runInput(run).getAll()), 2)
        for e in [x[0] for x in grrm2.runInput(run).getAll()]:
            try:
                molecule = grrm2.Molecule.get(e.graph(), e.uri())
            except:
                pass
            try:
                rundata = grrm2.RunData.get(e.graph(), e.uri())
                self.assertEqual(rundata.job(),"grrm")
                self.assertEqual(rundata.method(), "RHF")
                self.assertEqual(rundata.basisSet(), "6-31+G*")
            except:
                pass

        print graph.serialize()
        
if __name__ == '__main__':
    unittest.main()
    

