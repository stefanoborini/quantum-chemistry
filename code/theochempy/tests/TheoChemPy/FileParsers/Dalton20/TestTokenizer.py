# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens
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
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(tokens, [])
    # <<fold 
    def testTokenizer(self): # fold>>
        data = FileSnippets.fileHeader()+"\n"+ FileSnippets.centerOfMass()+"\n"+FileSnippets.isotopicMasses()+"\n"+FileSnippets.totalMass()+"\n"+FileSnippets.momentsOfInertia()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].__class__, Tokens.FileHeaderToken)
        self.assertEqual(tokens[1].__class__, Tokens.CenterOfMassToken)
        self.assertEqual(tokens[2].__class__, Tokens.IsotopicMassesToken)
        self.assertEqual(tokens[3].__class__, Tokens.TotalMassToken)
        self.assertEqual(tokens[4].__class__, Tokens.MomentsOfInertiaToken)
        # <<fold

    def testTokenizerFileHeader(self): # fold>>
        data = FileSnippets.fileHeader()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.FileHeaderToken)
        # <<fold
    def testTokenizerCenterOfMass(self): # fold>>
        data = FileSnippets.centerOfMass()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.CenterOfMassToken)
        # <<fold
    def testTokenizerIsotopicMasses(self): # fold>>
        data = FileSnippets.isotopicMasses()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.IsotopicMassesToken)
        # <<fold
    def testTokenizerTotalMass(self): # fold>>
        data = FileSnippets.totalMass()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.TotalMassToken)
        # <<fold
    def testTokenizerMomentsOfInertia(self): # fold>>
        data = FileSnippets.momentsOfInertia()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.MomentsOfInertiaToken)
        # <<fold
    def testTokenizerCartesianCoordinates(self): # fold>>
        data = FileSnippets.cartesianCoordinates()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.CartesianCoordinatesToken)
        # <<fold
    def testTokenizerEndOfOptimizationHeader(self): # fold>>
        data = FileSnippets.endOfOptimizationHeader()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.EndOfOptimizationHeaderToken)
        # <<fold
    def testTokenizerFinalGeometryEnergy(self): # fold>>
        data = FileSnippets.finalGeometryEnergy()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.FinalGeometryEnergyToken)
        # <<fold
    def testTokenizerGeometryConvergenceNumIterations(self): # fold>>
        data = FileSnippets.geometryConvergenceNumIterations()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.GeometryConvergenceNumIterationsToken)
        # <<fold
    def testTokenizerOptimizationNextGeometry(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.OptimizationNextGeometryToken)
        # <<fold
    def testTokenizerOptimizationInfo(self): # fold>>
        data = FileSnippets.optimizationInfo()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.OptimizationInfoToken)
        # <<fold
    def testTokenizerNormalModesEigenvalues(self): # fold>>
        data = FileSnippets.normalModesEigenvalues()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.NormalModesEigenvaluesToken)
        # <<fold
    def testTokenizerAtomsAndBasisSetsTable(self): # fold>>
        data = FileSnippets.atomsAndBasisSetsTable()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.AtomsAndBasisSetsToken)
        # <<fold
    def testTokenizerFinalGeometry(self): # fold>>
        data = FileSnippets.finalGeometry()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.FinalGeometryToken)
        # <<fold
    def testTokenizerDipoleMoment(self): # fold>>
        data = FileSnippets.dipoleMoment()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.DipoleMomentToken)
        # <<fold
    def testTokenizerDipoleMomentComponents(self): # fold>>
        data = FileSnippets.dipoleMomentComponents()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.DipoleMomentComponentsToken)
        # <<fold
    def testTokenizerHOMOLUMOSeparation(self): # fold>>
        data = FileSnippets.HomoLumoSeparation()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.HOMOLUMOSeparationToken)
        # <<fold
    def testTokenizerSymmetry(self): # fold>>
        data = FileSnippets.symmetry()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.SymmetryToken)
        # <<fold
    def testTokenizerResponseHeader(self): # fold>>
        data = FileSnippets.responseHeader()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.ResponseHeaderToken)
        # <<fold
    def testTokenizerFirstHyperpolarizabilityComponent(self): # fold>>
        data = FileSnippets.firstHyperpolarizability()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.FirstHyperpolarizabilityComponentToken)
        # <<fold
    def testTokenizerSecondHyperpolarizability(self): # fold>>
        data = FileSnippets.secondHyperpolarizability()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.SecondHyperpolarizabilityToken)
        # <<fold
    def testTokenizerSevereError(self): # fold>>
        data = FileSnippets.severeError()+"\n"
        writeToTestFile(data)
        tokens = Dalton20.tokenizeOutFile(testFilePath())

        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].__class__, Tokens.SevereErrorToken)
        # <<fold

if __name__ == '__main__':
    unittest.main()
    
