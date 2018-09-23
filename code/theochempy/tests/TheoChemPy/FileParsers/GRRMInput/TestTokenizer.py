# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy.FileParsers import GRRM
from theochempy._theochempy.FileParsers.GRRM import Tokens
from theochempy._theochempy.IO import FileReader

import FileSnippets

def moduleDir():
    return os.path.dirname(__file__)

def testFilePath():
    return os.path.join(moduleDir(), "testfile-TestTokenizer")
def writeToTestFile(data):
    f = file(testFilePath(), "w")
    f.write(data)
    f.close()
    
class TestTokenizer(unittest.TestCase):
    def testTokenizerEmptyFile(self): # fold>>
        writeToTestFile("")
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(tokens, [])
    # <<fold 

    def testHeaderDissociatedToken(self): # fold>>
        data = FileSnippets.headerDissociated()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.HeaderDissociatedToken)
        # <<fold

    def testHeaderEquilibriumToken(self): # fold>>
        data = FileSnippets.headerEquilibrium()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.HeaderEquilibriumToken)
        # <<fold

    def testHeaderTransitionToken(self): # fold>>
        data = FileSnippets.headerTransition()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.HeaderTransitionToken)
        # <<fold

    def testStructureHeaderToken(self): # fold>>
        data = FileSnippets.structureHeader()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.StructureHeaderToken)
        # <<fold

    def testGeometryToken(self): # fold>>
        data = FileSnippets.geometry()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.GeometryToken)
        # <<fold

    def testEnergyToken(self): # fold>>
        data = FileSnippets.energy()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.EnergyToken)
        # <<fold

    def testSpinToken(self): # fold>>
        data = FileSnippets.spin()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.SpinToken)
        # <<fold

    def testZPVEToken(self): # fold>>
        data = FileSnippets.zpve()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.ZPVEToken)
        # <<fold

    def testNormalModesToken(self): # fold>>
        data = FileSnippets.normalModes()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.NormalModesToken)
        # <<fold

    def testConnectionToken(self): # fold>>
        data = FileSnippets.connection()+"\n"
        writeToTestFile(data)
        tokens = GRRM.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.ConnectionToken)
        # <<fold

if __name__ == '__main__':
    unittest.main()

