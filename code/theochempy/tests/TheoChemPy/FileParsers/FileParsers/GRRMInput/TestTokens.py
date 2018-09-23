# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy.FileParsers.GRRMInput import Tokens
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
    def testCommandDirectiveToken(self): # fold>>
        data = FileSnippets.commandDirective()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CommandDirectiveToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.CommandDirectiveToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.commandLine(), "grrm/RHF/6-31+G*")
        self.assertEqual(token.jobString(), "grrm")
        self.assertEqual(token.methodString(), "RHF")
        self.assertEqual(token.basisSetString(), "6-31+G*")
        # <<fold
    def testGeometryToken(self): # fold>>
        data = FileSnippets.molecule()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.GeometryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.GeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+5)
        self.assertEqual(len(token.atomList()), 4)
        self.assertEqual(token.charge(), 0)
        self.assertEqual(token.spin(), 1)
        # <<fold
    def testOptionsHeaderToken(self): # fold>>
        data = FileSnippets.optionsHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.OptionsHeaderToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.OptionsHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testNRunOptionToken(self): # fold>>
        data = FileSnippets.nrunOption()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.NRunOptionToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.NRunOptionToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.value(), 4)
        # <<fold


if __name__ == '__main__':
    unittest.main()
    
