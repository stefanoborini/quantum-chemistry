# @author Stefano Borini
import os
import sys
import unittest

from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes
from wavemol.core import io

from . import filesnippets

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
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        self.assertEqual(list(token_gen), [])
    # <<fold 
    def testHeaderDissociatedToken(self): # fold>>
        data = filesnippets.headerDissociated()+"\n"
        writeToTestFile(data)
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)
        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.HeaderDissociatedToken)
        # <<fold
    def testHeaderEquilibriumToken(self): # fold>>
        data = filesnippets.headerEquilibrium()+"\n"
        writeToTestFile(data)

        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.HeaderEquilibriumToken)
        # <<fold
    def testHeaderTransitionToken(self): # fold>>
        data = filesnippets.headerTransition()+"\n"
        writeToTestFile(data)
 
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.HeaderTransitionToken)
        # <<fold
    def testStructureHeaderToken(self): # fold>>
        data = filesnippets.structureHeader()+"\n"
        writeToTestFile(data)
  
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.StructureHeaderToken)
        # <<fold
    def testGeometryToken(self): # fold>>
        data = filesnippets.geometry()+"\n"
        writeToTestFile(data)
   
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.GeometryToken)
        # <<fold
    def testEnergyToken(self): # fold>>
        data = filesnippets.energy()+"\n"
        writeToTestFile(data)
    
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.EnergyToken)
        # <<fold
    def testSpinToken(self): # fold>>
        data = filesnippets.spin()+"\n"
        writeToTestFile(data)
     
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.SpinToken)
        # <<fold
    def testZPVEToken(self): # fold>>
        data = filesnippets.zpve()+"\n"
        writeToTestFile(data)
      
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.ZPVEToken)
        # <<fold
    def testNormalModesToken(self): # fold>>
        data = filesnippets.normalModes()+"\n"
        writeToTestFile(data)
       
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.NormalModesToken)
        # <<fold
    def testConnectionToken(self): # fold>>
        data = filesnippets.connection()+"\n"
        writeToTestFile(data)
        
        tokenizer = grrm.ListOutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.ConnectionToken)
        # <<fold

