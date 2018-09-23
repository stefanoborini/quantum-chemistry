# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from TheoChemPy.FileParsers.Dalton import Tokens
from TheoChemPy.IO import FileReader

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

    def testFileHeaderToken(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FileHeaderToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.FileHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testCenterOfMassToken(self): # fold>>
        data = FileSnippets.centerOfMass()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CenterOfMassToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.CenterOfMassToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
        self.assertEqual(type(token.centerOfMass()), type(()))
        self.assertEqual(len(token.centerOfMass()), 3)
        self.assertEqual(token.centerOfMass()[0], "0.000000")
        self.assertEqual(token.centerOfMass()[1], "1.000000")
        self.assertEqual(token.centerOfMass()[2], "1.223609")
        
         
         # <<fold
    def testIsotopicMassesToken(self): # fold>>
        data = FileSnippets.isotopicMasses()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.IsotopicMassesToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.IsotopicMassesToken)
        self.assertEqual(reader.currentPos(), start_pos+8)
       
        atom_list = token.atomList()
        self.assertEqual(type(atom_list), type([]))
        self.assertEqual(len(atom_list), 4)
        self.assertEqual(atom_list[0], ("O1","", "15.994915"))
        self.assertEqual(atom_list[1], ("H1","1", "1.007825"))
        self.assertEqual(atom_list[2], ("H1","2", "1.007825"))
        self.assertEqual(atom_list[3], ("C1","", "12.000000"))
        
        # <<fold
    def testTotalMassToken(self): # fold>>
        data = FileSnippets.totalMass()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.TotalMassToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.TotalMassToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertEqual(type(token.totalMass()), type(""))
        self.assertEqual(token.totalMass(), "30.010565")
    # <<fold
    def testMomentsOfInertiaToken(self): # fold>>
        data = FileSnippets.momentsOfInertia()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.MomentsOfInertiaToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.MomentsOfInertiaToken)
        self.assertEqual(reader.currentPos(), start_pos+7)

        moments = token.momentsOfInertia()
        self.assertEqual(moments[0], "1.747844")
        self.assertEqual(moments[1], "13.208584")
        self.assertEqual(moments[2], "14.956428")
   
        principal_axes = token.principalAxes()
        for i,j in [(0,0), (0,1), (1,0), (1,2), (2,1), (2,2)]:
            self.assertEqual(principal_axes[i][j], "0.000000")
        for i,j in [(0,2), (1,1), (0,2)]:
            self.assertEqual(principal_axes[i][j], "1.000000")

        # <<fold
    def testCartesianCoordinatesToken(self): # fold>>
        data = FileSnippets.cartesianCoordinates()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CartesianCoordinatesToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.CartesianCoordinatesToken)
        self.assertEqual(reader.currentPos(), start_pos+22)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 4)

        self.assertEqual(atom_list[0][0], "O1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2], ("0.0000000000","0.0000000000","0.3000000000"))
   
        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2], ("0.0000000000","-1.7597098488","3.3775957364"))

        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2], ("0.0000000000","1.7597098488","3.3775957364"))

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2], ("0.0000000000","0.0000000000","2.3051919000"))

        # <<fold
    def testEndOfOptimizationHeaderToken(self): # fold>>
        data = FileSnippets.endOfOptimizationHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.EndOfOptimizationHeaderToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.EndOfOptimizationHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testFinalGeometryEnergyToken(self): # fold>>
        data = FileSnippets.finalGeometryEnergy()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FinalGeometryEnergyToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.FinalGeometryEnergyToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
       
        energy = token.energy()
        self.assertEqual(type(energy), type(""))
        self.assertEqual(energy,"-113.984888")
        
        # <<fold
    def testGeometryConvergenceNumIterationsToken(self): # fold>>
        data = FileSnippets.geometryConvergenceNumIterations()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.GeometryConvergenceNumIterationsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.GeometryConvergenceNumIterationsToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
       
        iterations = token.iterations()
        self.assertEqual(type(iterations), type(1))
        self.assertEqual(iterations,8)
        
        # <<fold
    def testOptimizationNextGeometryToken(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.OptimizationNextGeometryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.OptimizationNextGeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+8)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 4)

        self.assertEqual(atom_list[0][0], "O1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2], ("0.0000000000","0.0000000000","0.0680928675"))
   
        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2], ("0.0000000000","-1.7554324515","3.4700805319"))

        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2], ("0.0000000000","1.7554324515","3.4700805319"))

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2], ("0.0000000000","0.0000000000","2.3521294415"))

        # <<fold
    def testOptimizationInfoToken(self): # fold>>
        data = FileSnippets.optimizationInfo()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.OptimizationInfoToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.OptimizationInfoToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(token.iteration(), 0)
        self.assertEqual(token.endOfOptimization(), False)
        self.assertEqual(token.energy(), "-113.932636")
        self.assertEqual(token.energyChange(), None)
        self.assertEqual(token.gradientNorm(), "0.567825")
        self.assertEqual(token.stepNorm(), "0.487002")
        self.assertEqual(token.trustRadius(), "0.500000")
        self.assertEqual(token.totalHessianIndex(), 0)

        # <<fold
    def testOptimizationInfoToken2(self): # fold>>
        data = FileSnippets.optimizationInfo2()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.OptimizationInfoToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.OptimizationInfoToken)
        self.assertEqual(reader.currentPos(), start_pos+11)

        self.assertEqual(token.iteration(), 1)
        self.assertEqual(token.endOfOptimization(), True)
        self.assertEqual(token.energy(), "-113.984495")
        self.assertEqual(token.energyChange(), "-0.051859")
        self.assertEqual(token.gradientNorm(), "0.030306")
        self.assertEqual(token.stepNorm(), "0.030552")
        self.assertEqual(token.trustRadius(), "0.584403")
        self.assertEqual(token.totalHessianIndex(), 0)

        # <<fold
    def testNormalModesEigenvaluesToken(self): # fold>>
        data = FileSnippets.normalModesEigenvalues()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.NormalModesEigenvaluesToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.NormalModesEigenvaluesToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(len(token.values()), 6)
        for index, correct_value in enumerate([1.279649E-42,1.279649E-42,4.094095E-04,9.790871E-44,9.790871E-44, -1.212226E-21]):
            self.assertAlmostEqual(token.values()[index], correct_value)

        # <<fold
    def testAtomsAndBasisSetsToken(self): # fold>>
        data = FileSnippets.atomsAndBasisSetsTable()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.AtomsAndBasisSetsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.AtomsAndBasisSetsToken)
        self.assertEqual(reader.currentPos(), start_pos+22)

        self.assertEqual(token.totalNumberOfAtoms(), 10)
        self.assertEqual(token.numOfAtomTypes(), 2)
        self.assertEqual(len(token.atomDataList()), 10)

        self.assertEqual(token.atomDataList()[0][0], "H1")
        self.assertEqual(token.atomDataList()[0][1], 1)
        self.assertEqual(token.atomDataList()[0][2], 1)
        self.assertEqual(token.atomDataList()[0][3], 7)
        self.assertEqual(token.atomDataList()[0][4], 5)
        self.assertEqual(token.atomDataList()[0][5], "[4s1p|2s1p]")

        self.assertEqual(token.atomDataList()[5][0], "H6")
        self.assertEqual(token.atomDataList()[5][1], 1)
        self.assertEqual(token.atomDataList()[5][2], 1)
        self.assertEqual(token.atomDataList()[5][3], 7)
        self.assertEqual(token.atomDataList()[5][4], 5)
        self.assertEqual(token.atomDataList()[5][5], "[4s1p|2s1p]")

        self.assertEqual(token.atomDataList()[6][0], "C1")
        self.assertEqual(token.atomDataList()[6][1], 1)
        self.assertEqual(token.atomDataList()[6][2], 6)
        self.assertEqual(token.atomDataList()[6][3], 26)
        self.assertEqual(token.atomDataList()[6][4], 14)
        self.assertEqual(token.atomDataList()[6][5], "[9s4p1d|3s2p1d]")

        self.assertEqual(token.atomDataList()[9][0], "C4")
        self.assertEqual(token.atomDataList()[9][1], 1)
        self.assertEqual(token.atomDataList()[9][2], 6)
        self.assertEqual(token.atomDataList()[9][3], 26)
        self.assertEqual(token.atomDataList()[9][4], 14)
        self.assertEqual(token.atomDataList()[9][5], "[9s4p1d|3s2p1d]")

        # <<fold
    def testFinalGeometryToken(self): # fold>>
        data = FileSnippets.finalGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FinalGeometryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.FinalGeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+14)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 10)

        self.assertEqual(atom_list[0][0], "H1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2], ("0.0000002307","-0.0431166985","-0.0202403617"))
   
        self.assertEqual(atom_list[1][0], "H2")
        self.assertEqual(atom_list[1][1], "")
        self.assertEqual(atom_list[1][2], ("0.0000001751","1.6729220095" ,"-3.0984614789"))

        self.assertEqual(atom_list[2][0], "H3")
        self.assertEqual(atom_list[2][1], "")
        self.assertEqual(atom_list[2][2], ("-0.0000000621","3.9834654382","2.2591198806"))

        self.assertEqual(atom_list[3][0], "H4")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2], ("-0.0000004152","6.3971763363","-3.1312282876"))

        self.assertEqual(atom_list[4][0], "H5")
        self.assertEqual(atom_list[4][1], "")
        self.assertEqual(atom_list[4][2], ("0.0000000584" ,"8.7077203406","2.2263528516"))

        self.assertEqual(atom_list[5][0], "H6")
        self.assertEqual(atom_list[5][1], "")
        self.assertEqual(atom_list[5][2], ("0.0000011485", "10.4237584759","-0.8518686398"))

        self.assertEqual(atom_list[6][0], "C1")
        self.assertEqual(atom_list[6][1], "")
        self.assertEqual(atom_list[6][2], ("0.0000002040", "1.7527241877","-1.0336061328"))

        self.assertEqual(atom_list[7][0], "C2")
        self.assertEqual(atom_list[7][1], "")
        self.assertEqual(atom_list[7][2], ("-0.0000000301","3.9601114154","0.1889860925"))

        self.assertEqual(atom_list[8][0], "C3")
        self.assertEqual(atom_list[8][1], "")
        self.assertEqual(atom_list[8][2], ("-0.0000005431","6.4205305038","-1.0610944968"))

        self.assertEqual(atom_list[9][0], "C4")
        self.assertEqual(atom_list[9][1], "")
        self.assertEqual(atom_list[9][2], ("-0.0000007662","8.6279178237","0.1614975188" ))

        # <<fold
    def testDipoleMomentToken(self): # fold>>
        data = FileSnippets.dipoleMoment()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.DipoleMomentToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.DipoleMomentToken)
        self.assertEqual(reader.currentPos(), start_pos+4)

        dipole = token.dipole()

        self.assertAlmostEqual(dipole, 3.141592)

        # <<fold
    def testDipoleMomentsComponents(self): # fold>>
        data = FileSnippets.dipoleMomentComponents()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.DipoleMomentComponentsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.DipoleMomentComponentsToken)
        self.assertEqual(reader.currentPos(), start_pos+8)

        dipole = token.dipole()

        self.assertAlmostEqual(dipole[0], 3.14159270)
        self.assertAlmostEqual(dipole[1], -1.23456789)
        self.assertAlmostEqual(dipole[2], 9.87654321)
        # <<fold
    def testHOMOLUMOSeparationToken(self): # fold>>
        data = FileSnippets.HomoLumoSeparation()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.HOMOLUMOSeparationToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.HOMOLUMOSeparationToken)
        self.assertEqual(reader.currentPos(), start_pos+4)

        lumo_energy = token.LUMOEnergy()
        homo_energy = token.HOMOEnergy()
        lumo_symmetry = token.LUMOSymmetry()
        homo_symmetry = token.HOMOSymmetry()
        gap = token.gap()

        self.assertAlmostEqual(lumo_energy, 0.01936070)
        self.assertEqual(lumo_symmetry, 1)
        self.assertEqual(homo_symmetry, 1)
        self.assertAlmostEqual(homo_energy, -0.28830940)
        self.assertAlmostEqual(gap, 0.30767010)
        # <<fold
    def testBondLengthsToken(self): # fold>>
        data = FileSnippets.bondLengths()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.BondLengthsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.BondLengthsToken)
        self.assertEqual(reader.currentPos(), start_pos+15)

        self.assertEqual(len(token.atomList()), 9)

        self.assertEqual(token.atomList()[0][0][0], "C2")
        self.assertEqual(token.atomList()[0][0][1], "1")
        self.assertEqual(token.atomList()[0][1][0], "H1")
        self.assertEqual(token.atomList()[0][1][1], "1")
        self.assertEqual(token.atomList()[0][2], "1.091176")

        self.assertEqual(token.atomList()[8][0][0], "C4")
        self.assertEqual(token.atomList()[8][0][1], "2")
        self.assertEqual(token.atomList()[8][1][0], "C4")
        self.assertEqual(token.atomList()[8][1][1], "1")
        self.assertEqual(token.atomList()[8][2], "1.460430")

        # <<fold
        
    def testFileHeaderTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile("\n"+data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FileHeaderToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
        # <<fold
    def testCenterOfMassTokenNotMatching(self): # fold>>
        data = FileSnippets.centerOfMass()
        writeToTestFile("\n"+data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CenterOfMassToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
         # <<fold
    def testIsotopicMassesTokenNotMatching(self): # fold>>
        data = FileSnippets.isotopicMasses()
        writeToTestFile("\n"+data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.IsotopicMassesToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
        # <<fold
    def testTotalMassTokenNotMatching(self): # fold>>
        data = FileSnippets.totalMass()
        writeToTestFile("\n"+data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.TotalMassToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
        # <<fold 
    def testMomentsOfInertiaTokenNotMatching(self): # fold>>
        data = FileSnippets.momentsOfInertia()
        writeToTestFile("\n"+data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.MomentsOfInertiaToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
        # <<fold
    def testCartesianCoordinatesTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CartesianCoordinatesToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testEndOfOptimizationHeaderTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.EndOfOptimizationHeaderToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
        # <<fold
    def testFinalGeometryEnergyTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FinalGeometryEnergyToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
        # <<fold
    def testGeometryConvergenceNumIterationsTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.GeometryConvergenceNumIterationsToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)
       
        # <<fold
    def testOptimizationNextGeometryTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.OptimizationNextGeometryToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testOptimizationInfoTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.OptimizationInfoToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testNormalModesEigenvaluesTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.NormalModesEigenvaluesToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testAtomsAndBasisSetsTokenNotMatching(self): # fold>>
        data = FileSnippets.fileHeader()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.AtomsAndBasisSetsToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testFinalGeometryTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FinalGeometryToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testDipoleMomentTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.DipoleMomentToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testDipoleMomentComponentsTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.DipoleMomentComponentsToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testHOMOLUMOSeparationTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.HOMOLUMOSeparationToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold

    def testTryReadColumnHeader(self): # fold>>
        self.assertEqual(Tokens._tryReadColumnHeader(""), None)
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5"), [5])
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6"), [5,6])
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6  "), [5,6])
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6 boo "), None)
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6 Column 7"), [5,6,7])
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6 Column 7 Column 8"), [5,6,7,8])
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6 Column 7 Column 8 Column 9"), [5,6,7,8,9])
        self.assertEqual(Tokens._tryReadColumnHeader(" Column 5 Column 6 Column 7 Column x"), None)
        self.assertEqual(Tokens._tryReadColumnHeader(" Column x Column 6 Column 7 Column x"), None)
        # <<fold
    def testTryReadRowValues(self): # fold>>
        self.assertEqual(Tokens._tryReadRowValues(""), None)

        t = Tokens._tryReadRowValues("  1     1.279649E-02   5.279649E-02   4.094095E-04   3.790871E-04 ")
        self.assertNotEqual(t, None)
        self.assertEqual(len(t), 2)
        index, values = t
        self.assertEqual(index, 1)
        self.assertEqual(len(values), 4)
        self.assertAlmostEqual(values[0], 1.279649E-02)
        self.assertAlmostEqual(values[1], 5.279649E-02)
        self.assertAlmostEqual(values[2], 4.094095E-04)
        self.assertAlmostEqual(values[3], 3.790871E-04)
        
        t = Tokens._tryReadRowValues("  1     1.279649E-02 x  5.279649E-02   4.094095E-04   3.790871E-04 ")
        self.assertEqual(t, None)

        t = Tokens._tryReadRowValues("  1     1.279649E-02  ")
        self.assertNotEqual(t, None)
        self.assertEqual(len(t), 2)
        index, values = t
        self.assertEqual(index, 1)
        self.assertEqual(len(values), 1)
        self.assertAlmostEqual(values[0], 1.279649E-02)
        # <<fold

if __name__ == '__main__':
    unittest.main()
    
