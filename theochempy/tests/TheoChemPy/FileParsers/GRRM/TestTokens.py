# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy.FileParsers.GRRM import Tokens
from theochempy._theochempy.IO import FileReader
from theochempy._theochempy import Units
from theochempy._theochempy import Measure

import FileSnippets

def moduleDir():
    return os.path.dirname(__file__)

def testFilePath():
    return os.path.join(moduleDir(), "testfile-TestTokens")
def writeToTestFile(data):
    f = file(testFilePath(), "w")
    f.write(data)
    f.close()
    
class TestTokens(unittest.TestCase):
    def testHeaderDissociatedToken(self): # fold>>
        data = FileSnippets.headerDissociated()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.HeaderDissociatedToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.HeaderDissociatedToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testHeaderEquilibriumToken(self): # fold>>
        data = FileSnippets.headerEquilibrium()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.HeaderEquilibriumToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.HeaderEquilibriumToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testHeaderTransitionToken(self): # fold>>
        data = FileSnippets.headerTransition()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.HeaderTransitionToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.HeaderTransitionToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testStructureHeaderToken(self): # fold>>
        data = FileSnippets.structureHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.StructureHeaderToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.StructureHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.type(), "DC")
        self.assertEqual(token.number(), 1)
        self.assertEqual(token.symmetry(), "C1")
        # <<fold
    def testGeometryToken(self): # fold>>
        data = FileSnippets.geometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.GeometryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.GeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+9)
        self.assertEqual(len(token.atomList()), 9 )
        # <<fold
    def testEnergyToken(self): # fold>>
        data = FileSnippets.energy()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.EnergyToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.EnergyToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertAlmostEqual(token.energy().value(), -153.869550889154 )
        # <<fold
    def testSpinToken(self): # fold>>
        data = FileSnippets.spin()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SpinToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.SpinToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertAlmostEqual(token.spin().value(), 0.0 )
        # <<fold
    def testZPVEToken(self): # fold>>
        data = FileSnippets.zpve()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.ZPVEToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.ZPVEToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertAlmostEqual(token.zpve().value(), 0.074920061481 )
        # <<fold
    def testNormalModesToken(self): # fold>>
        data = FileSnippets.normalModes()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.NormalModesToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.NormalModesToken)
        self.assertEqual(reader.currentPos(), start_pos+5)
        self.assertEqual(len(token.eigenvalues()), 20 )
        # <<fold
    def testConnectionToken(self): # fold>>
        data = FileSnippets.connection()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.ConnectionToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.ConnectionToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.first(), "0" )
        self.assertEqual(token.second(), "DC" )
        # <<fold


if __name__ == '__main__':
    unittest.main()
    
