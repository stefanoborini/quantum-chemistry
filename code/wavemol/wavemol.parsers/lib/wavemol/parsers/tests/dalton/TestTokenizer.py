# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from wavemol.parsers import dalton 
from wavemol.parsers.dalton import tokentypes
from wavemol.parsers.tests.dalton import filesnippets

def moduleDir():
    return os.path.dirname(__file__)

def testFilePath():
    return os.path.join(moduleDir(), "testfile-TestTokenizer")
def writeToTestFile(data):
    f = file(testFilePath(), "w")
    f.write(data)
    f.close()
    
class TestOutputTokenizer(unittest.TestCase):
    def testTokenizerEmptyFile(self): # fold>>
        writeToTestFile("")
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())

        self.assertEqual(list(token_gen), [])
    # <<fold 
    def testTokenizer(self): # fold>>
        data = filesnippets.fileHeader()+"\n"+ filesnippets.centerOfMass()+"\n"+filesnippets.isotopicMasses()+"\n"+filesnippets.totalMass()+"\n"+filesnippets.momentsOfInertia()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)
        self.assertEqual(len(token_list), 5)
        self.assertEqual(token_list[0].__class__, tokentypes.FileHeaderToken)
        self.assertEqual(token_list[1].__class__, tokentypes.CenterOfMassToken)
        self.assertEqual(token_list[2].__class__, tokentypes.IsotopicMassesToken)
        self.assertEqual(token_list[3].__class__, tokentypes.TotalMassToken)
        self.assertEqual(token_list[4].__class__, tokentypes.MomentsOfInertiaToken)
        # <<fold
    def testTokenizerFileHeader(self): # fold>>
        data = filesnippets.fileHeader()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)
        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.FileHeaderToken)
        # <<fold
    def testTokenizerCenterOfMass(self): # fold>>
        data = filesnippets.centerOfMass()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.CenterOfMassToken)
        # <<fold
    def testTokenizerIsotopicMasses(self): # fold>>
        data = filesnippets.isotopicMasses()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.IsotopicMassesToken)
        # <<fold
    def testTokenizerTotalMass(self): # fold>>
        data = filesnippets.totalMass()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.TotalMassToken)
        # <<fold
    def testTokenizerMomentsOfInertia(self): # fold>>
        data = filesnippets.momentsOfInertia()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.MomentsOfInertiaToken)
        # <<fold
    def testTokenizerCartesianCoordinates(self): # fold>>
        data = filesnippets.cartesianCoordinates()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.CartesianCoordinatesToken)
        # <<fold
    def testTokenizerEndOfOptimizationHeader(self): # fold>>
        data = filesnippets.endOfOptimizationHeader()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.EndOfOptimizationHeaderToken)
        # <<fold
    def testTokenizerFinalGeometryEnergy(self): # fold>>
        data = filesnippets.finalGeometryEnergy()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.FinalGeometryEnergyToken)
        # <<fold
    def testTokenizerGeometryConvergenceNumIterations(self): # fold>>
        data = filesnippets.geometryConvergenceNumIterations()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.GeometryConvergenceNumIterationsToken)
        # <<fold
    def testTokenizerOptimizationNextGeometry(self): # fold>>
        data = filesnippets.optimizationNextGeometry()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.OptimizationNextGeometryToken)
        # <<fold
    def testTokenizerOptimizationInfo(self): # fold>>
        data = filesnippets.optimizationInfo()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.OptimizationInfoToken)
        # <<fold
    def testTokenizerNormalModesEigenvalues(self): # fold>>
        data = filesnippets.normalModesEigenvalues()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.NormalModesEigenvaluesToken)
        # <<fold
    def testTokenizerAtomsAndBasisSetsTable(self): # fold>>
        data = filesnippets.atomsAndBasisSetsTable()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.AtomsAndBasisSetsToken)
        # <<fold
    def testTokenizerFinalGeometry(self): # fold>>
        data = filesnippets.finalGeometry()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.FinalGeometryToken)
        # <<fold
    def testTokenizerDipoleMoment(self): # fold>>
        data = filesnippets.dipoleMoment()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.DipoleMomentToken)
        # <<fold
    def testTokenizerDipoleMomentComponents(self): # fold>>
        data = filesnippets.dipoleMomentComponents()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.DipoleMomentComponentsToken)
        # <<fold
    def testTokenizerHOMOLUMOSeparation(self): # fold>>
        data = filesnippets.HomoLumoSeparation()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.HOMOLUMOSeparationToken)
        # <<fold
    def testTokenizerSymmetry(self): # fold>>
        data = filesnippets.symmetry()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.SymmetryToken)
        # <<fold
    def testTokenizerResponseHeader(self): # fold>>
        data = filesnippets.responseHeader()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.ResponseHeaderToken)
        # <<fold
    def testTokenizerFirstHyperpolarizabilityComponent(self): # fold>>
        data = filesnippets.firstHyperpolarizability()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.FirstHyperpolarizabilityComponentToken)
        # <<fold
    def testTokenizerSecondHyperpolarizability(self): # fold>>
        data = filesnippets.secondHyperpolarizability()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.SecondHyperpolarizabilityToken)
        # <<fold
    def testTokenizerSevereError(self): # fold>>
        data = filesnippets.severeError()+"\n"
        writeToTestFile(data)
        tokenizer = dalton.OutputTokenizer()
        token_gen = tokenizer.tokenize(testFilePath())
        token_list = list(token_gen)

        self.assertEqual(len(token_list), 1)
        self.assertEqual(token_list[0].__class__, tokentypes.SevereErrorToken)
        # <<fold


if __name__ == '__main__':
    unittest.main()
    
