# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy.FileParsers.Dalton20 import Tokens
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
        
        self.assertEqual(token.centerOfMass().__class__, Measure.Measure)
        self.assertEqual(len(token.centerOfMass().value()), 3)
        self.assertAlmostEqual(token.centerOfMass().value()[0], 0.000000)
        self.assertAlmostEqual(token.centerOfMass().value()[1], 1.000000)
        self.assertAlmostEqual(token.centerOfMass().value()[2], 1.223609)
        self.assertEqual(token.centerOfMass().unit(), Units.bohr)
        
         
         # <<fold
    def testTotalMassToken(self): # fold>>
        data = FileSnippets.totalMass()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.TotalMassToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.TotalMassToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertEqual(token.totalMass().__class__, Measure.Measure )
        self.assertEqual(token.totalMass().value(), 30.010565)
        self.assertEqual(token.totalMass().unit(), Units.dalton)
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

        self.assertEqual(atom_list[0][0], "O1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[0][2].value(), 15.994915)
        self.assertEqual(atom_list[0][2].unit(), Units.dalton)

        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2].__class__, Measure.Measure )
        self.assertEqual(atom_list[1][2].value(), 1.007825)
        self.assertEqual(atom_list[1][2].unit(), Units.dalton)

        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2].__class__, Measure.Measure )
        self.assertEqual(atom_list[2][2].value(), 1.007825)
        self.assertEqual(atom_list[2][2].unit(), Units.dalton)

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, Measure.Measure )
        self.assertEqual(atom_list[3][2].value(), 12.0000)
        self.assertEqual(atom_list[3][2].unit(), Units.dalton)
        
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
        self.assertEqual(moments.__class__, list)

        self.assertEqual(moments[0].value(), 1.747844)
        self.assertEqual(moments[1].value(), 13.208584)
        self.assertEqual(moments[2].value(), 14.956428)
        for i in xrange(0,3):
            self.assertEqual(moments[i].unit(), Units.dalton * Units.angstrom * Units.angstrom)

        principal_axes = token.principalAxes()
        self.assertEqual(principal_axes.__class__, list)
        for i,j in [(0,0), (0,1), (1,0), (1,2), (2,1), (2,2)]:
            self.assertEqual(principal_axes[i].value()[j], 0.000000)
        for i,j in [(0,2), (1,1), (0,2)]:
            self.assertEqual(principal_axes[i].value()[j], 1.000000)

        for i in [0,1,2]:
            self.assertEqual(principal_axes[i].unit(), Units.angstrom)
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
        self.assertEqual(atom_list[0][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[0][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[0][2].value()[1], 0.0000000000)
        self.assertEqual(atom_list[0][2].value()[2], 0.3000000000)
        self.assertEqual(atom_list[0][2].unit(), Units.bohr)
   
        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[1][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[1][2].value()[1],-1.7597098488)
        self.assertEqual(atom_list[1][2].value()[2],3.3775957364)
        self.assertEqual(atom_list[1][2].unit(), Units.bohr)


        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[2][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[2][2].value()[1], 1.7597098488)
        self.assertEqual(atom_list[2][2].value()[2], 3.3775957364)
        self.assertEqual(atom_list[2][2].unit(), Units.bohr)

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[3][2].value()[0],0.0000000000)
        self.assertEqual(atom_list[3][2].value()[1],0.0000000000)
        self.assertEqual(atom_list[3][2].value()[2],2.3051919000)
        self.assertEqual(atom_list[3][2].unit(), Units.bohr)

        # <<fold
    def testCartesianCoordinatesToken2(self): # fold>>
        data = FileSnippets.cartesianCoordinates2()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CartesianCoordinatesToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.CartesianCoordinatesToken)
        self.assertEqual(reader.currentPos(), start_pos+53)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 12)

        # <<fold
    def testCartesianCoordinatesToken3(self): # fold>>
        data = FileSnippets.cartesianCoordinates3()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.CartesianCoordinatesToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.CartesianCoordinatesToken)
        self.assertEqual(reader.currentPos(), start_pos+181)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 44)

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
        self.assertEqual(energy.__class__, Measure.Measure)
        self.assertEqual(energy.value(),-113.984888)
        self.assertEqual(energy.unit(), Units.hartree)
        
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
        self.assertEqual(atom_list[0][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[0][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[0][2].value()[1], 0.0000000000)
        self.assertEqual(atom_list[0][2].value()[2], 0.0680928675)
        self.assertEqual(atom_list[0][2].unit(), Units.bohr)
   
        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[1][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[1][2].value()[1], -1.7554324515)
        self.assertEqual(atom_list[1][2].value()[2], 3.4700805319)
        self.assertEqual(atom_list[1][2].unit(), Units.bohr)

        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[2][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[2][2].value()[1], 1.7554324515)
        self.assertEqual(atom_list[2][2].value()[2], 3.4700805319)
        self.assertEqual(atom_list[2][2].unit(), Units.bohr)

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[3][2].value()[0], 0.0000000000)
        self.assertEqual(atom_list[3][2].value()[1], 0.0000000000)
        self.assertEqual(atom_list[3][2].value()[2], 2.3521294415)
        self.assertEqual(atom_list[3][2].unit(), Units.bohr)

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
        self.assertEqual(token.energy().__class__, Measure.Measure)
        self.assertEqual(token.energy().value(), -113.932636)
        self.assertEqual(token.energy().unit(), Units.hartree)
        self.assertEqual(token.energyChange(), None)
        self.assertEqual(token.gradientNorm().__class__, Measure.Measure)
        self.assertEqual(token.gradientNorm().value(), 0.567825)
        self.assertEqual(token.gradientNorm().unit(), Units.unknown)
        self.assertEqual(token.stepNorm().__class__, Measure.Measure)
        self.assertEqual(token.stepNorm().value(), 0.487002)
        self.assertEqual(token.stepNorm().unit(), Units.unknown)
        self.assertEqual(token.trustRadius().__class__, Measure.Measure)
        self.assertEqual(token.trustRadius().value(), 0.500000)
        self.assertEqual(token.trustRadius().unit(), Units.unknown)
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
        self.assertEqual(token.energy().__class__, Measure.Measure)
        self.assertEqual(token.energy().value(), -113.984495)
        self.assertEqual(token.energy().unit(), Units.hartree)
        self.assertEqual(token.energyChange().__class__, Measure.Measure)
        self.assertEqual(token.energyChange().value(), -0.051859)
        self.assertEqual(token.energyChange().unit(), Units.hartree)
        self.assertEqual(token.gradientNorm().__class__, Measure.Measure)
        self.assertEqual(token.gradientNorm().value(), 0.030306)
        self.assertEqual(token.gradientNorm().unit(), Units.unknown)
        self.assertEqual(token.stepNorm().__class__, Measure.Measure)
        self.assertEqual(token.stepNorm().value(), 0.030552)
        self.assertEqual(token.stepNorm().unit(), Units.unknown)
        self.assertEqual(token.trustRadius().__class__, Measure.Measure)
        self.assertEqual(token.trustRadius().value(), 0.584403)
        self.assertEqual(token.trustRadius().unit(), Units.unknown)
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
            self.assertAlmostEqual(token.values()[index].value(), correct_value)
            self.assertEqual(token.values()[index].unit(), Units.unknown)

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

        self.assertEqual(token.spherical(), True)
        self.assertEqual(token.basisSet(), None)

        # <<fold
    def testAtomsAndBasisSetsToken2(self): # fold>>
        data = FileSnippets.atomsAndBasisSetsTable2()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.AtomsAndBasisSetsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.AtomsAndBasisSetsToken)
        self.assertEqual(reader.currentPos(), start_pos+27)

        self.assertEqual(token.totalNumberOfAtoms(), 13)
        self.assertEqual(token.numOfAtomTypes(), 4)
        self.assertEqual(len(token.atomDataList()), 13)

        self.assertEqual(token.atomDataList()[0][0], "O1")
        self.assertEqual(token.atomDataList()[0][1], 1)
        self.assertEqual(token.atomDataList()[0][2], 8)
        self.assertEqual(token.atomDataList()[0][3], 26)
        self.assertEqual(token.atomDataList()[0][4], 14)
        self.assertEqual(token.atomDataList()[0][5], "[9s4p1d|3s2p1d]")

        self.assertEqual(token.atomDataList()[5][0], "H4")
        self.assertEqual(token.atomDataList()[5][1], 1)
        self.assertEqual(token.atomDataList()[5][2], 1)
        self.assertEqual(token.atomDataList()[5][3], 7)
        self.assertEqual(token.atomDataList()[5][4], 5)
        self.assertEqual(token.atomDataList()[5][5], "[4s1p|2s1p]")

        self.assertEqual(token.atomDataList()[6][0], "N1")
        self.assertEqual(token.atomDataList()[6][1], 1)
        self.assertEqual(token.atomDataList()[6][2], 7)
        self.assertEqual(token.atomDataList()[6][3], 26)
        self.assertEqual(token.atomDataList()[6][4], 14)
        self.assertEqual(token.atomDataList()[6][5], "[9s4p1d|3s2p1d]")

        self.assertEqual(token.atomDataList()[9][0], "C2")
        self.assertEqual(token.atomDataList()[9][1], 1)
        self.assertEqual(token.atomDataList()[9][2], 6)
        self.assertEqual(token.atomDataList()[9][3], 26)
        self.assertEqual(token.atomDataList()[9][4], 14)
        self.assertEqual(token.atomDataList()[9][5], "[9s4p1d|3s2p1d]")

        self.assertEqual(token.atomDataList()[12][0], "C5")
        self.assertEqual(token.atomDataList()[12][1], 1)
        self.assertEqual(token.atomDataList()[12][2], 6)
        self.assertEqual(token.atomDataList()[12][3], 26)
        self.assertEqual(token.atomDataList()[12][4], 14)
        self.assertEqual(token.atomDataList()[12][5], "[9s4p1d|3s2p1d]")

        self.assertEqual(token.spherical(), True)
        self.assertEqual(token.basisSet(), "cc-pVDZ")

        # <<fold
    def testAtomsAndBasisSetsToken3(self): # fold>>
        data = FileSnippets.atomsAndBasisSetsTable3()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.AtomsAndBasisSetsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.AtomsAndBasisSetsToken)

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
        self.assertEqual(atom_list[0][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[0][2].value()[0], 0.0000002307)
        self.assertEqual(atom_list[0][2].value()[1], -0.0431166985)
        self.assertEqual(atom_list[0][2].value()[2], -0.0202403617)
        self.assertEqual(atom_list[0][2].unit(), Units.bohr)
   
        self.assertEqual(atom_list[1][0], "H2")
        self.assertEqual(atom_list[1][1], "")
        self.assertEqual(atom_list[1][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[1][2].value()[0], 0.0000001751)
        self.assertEqual(atom_list[1][2].value()[1], 1.6729220095)
        self.assertEqual(atom_list[1][2].value()[2], -3.0984614789)
        self.assertEqual(atom_list[1][2].unit(), Units.bohr)

        self.assertEqual(atom_list[2][0], "H3")
        self.assertEqual(atom_list[2][1], "")
        self.assertEqual(atom_list[2][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[2][2].value()[0], -0.0000000621)
        self.assertEqual(atom_list[2][2].value()[1], 3.9834654382)
        self.assertEqual(atom_list[2][2].value()[2], 2.2591198806)
        self.assertEqual(atom_list[2][2].unit(), Units.bohr)

        self.assertEqual(atom_list[3][0], "H4")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[3][2].value()[0], -0.0000004152)
        self.assertEqual(atom_list[3][2].value()[1], 6.3971763363)
        self.assertEqual(atom_list[3][2].value()[2], -3.1312282876)
        self.assertEqual(atom_list[3][2].unit(), Units.bohr)

        self.assertEqual(atom_list[4][0], "H5")
        self.assertEqual(atom_list[4][1], "")
        self.assertEqual(atom_list[4][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[4][2].value()[0],0.0000000584)
        self.assertEqual(atom_list[4][2].value()[1],8.7077203406)
        self.assertEqual(atom_list[4][2].value()[2],2.2263528516)
        self.assertEqual(atom_list[4][2].unit(), Units.bohr)

        self.assertEqual(atom_list[5][0], "H6")
        self.assertEqual(atom_list[5][1], "")
        self.assertEqual(atom_list[5][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[5][2].value()[0], 0.0000011485)
        self.assertEqual(atom_list[5][2].value()[1], 10.4237584759)
        self.assertEqual(atom_list[5][2].value()[2], -0.8518686398)
        self.assertEqual(atom_list[5][2].unit(), Units.bohr)

        self.assertEqual(atom_list[6][0], "C1")
        self.assertEqual(atom_list[6][1], "")
        self.assertEqual(atom_list[6][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[6][2].value()[0], 0.0000002040)
        self.assertEqual(atom_list[6][2].value()[1], 1.7527241877)
        self.assertEqual(atom_list[6][2].value()[2], -1.0336061328)
        self.assertEqual(atom_list[6][2].unit(), Units.bohr)

        self.assertEqual(atom_list[7][0], "C2")
        self.assertEqual(atom_list[7][1], "")
        self.assertEqual(atom_list[7][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[7][2].value()[0], -0.0000000301)
        self.assertEqual(atom_list[7][2].value()[1], 3.9601114154)
        self.assertEqual(atom_list[7][2].value()[2], 0.1889860925)
        self.assertEqual(atom_list[7][2].unit(), Units.bohr)

        self.assertEqual(atom_list[8][0], "C3")
        self.assertEqual(atom_list[8][1], "")
        self.assertEqual(atom_list[8][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[8][2].value()[0], -0.0000005431)
        self.assertEqual(atom_list[8][2].value()[1], 6.4205305038)
        self.assertEqual(atom_list[8][2].value()[2], -1.0610944968)
        self.assertEqual(atom_list[8][2].unit(), Units.bohr)

        self.assertEqual(atom_list[9][0], "C4")
        self.assertEqual(atom_list[9][1], "")
        self.assertEqual(atom_list[9][2].__class__, Measure.Measure)
        self.assertEqual(atom_list[9][2].value()[0], -0.0000007662)
        self.assertEqual(atom_list[9][2].value()[1], 8.6279178237)
        self.assertEqual(atom_list[9][2].value()[2], 0.1614975188)
        self.assertEqual(atom_list[9][2].unit(), Units.bohr)

        # <<fold
    def testDipoleMomentToken(self): # fold>>
        data = FileSnippets.dipoleMoment()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.DipoleMomentToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.DipoleMomentToken)
        self.assertEqual(reader.currentPos(), start_pos+4)

        dipole = token.dipole().value()
        unit = token.dipole().unit()
        self.assertAlmostEqual(dipole, 3.1415927)
        self.assertEqual(unit, Units.debye)

        # <<fold
    def testDipoleMomentComponents(self): # fold>>
        data = FileSnippets.dipoleMomentComponents()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.DipoleMomentComponentsToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.DipoleMomentComponentsToken)
        self.assertEqual(reader.currentPos(), start_pos+8)

        dipole = token.dipole().value()
        unit = token.dipole().unit()

        self.assertAlmostEqual(dipole[0], 3.14159270)
        self.assertAlmostEqual(dipole[1], -1.23456789)
        self.assertAlmostEqual(dipole[2], 9.87654321)
        self.assertEqual(unit, Units.debye)
        # <<fold
    def testHOMOLUMOSeparationToken(self): # fold>>
        data = FileSnippets.HomoLumoSeparation()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.HOMOLUMOSeparationToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.HOMOLUMOSeparationToken)
        self.assertEqual(reader.currentPos(), start_pos+4)

        lumo_energy = token.LUMOEnergy().value()
        homo_energy = token.HOMOEnergy().value()
        lumo_symmetry = token.LUMOSymmetry()
        homo_symmetry = token.HOMOSymmetry()
        lumo_unit = token.LUMOEnergy().unit()
        homo_unit = token.LUMOEnergy().unit()

        gap = token.gap().value()
        gap_unit = token.gap().unit()

        self.assertAlmostEqual(lumo_energy, 0.01936070)
        self.assertEqual(lumo_symmetry, 1)
        self.assertEqual(homo_symmetry, 1)
        self.assertAlmostEqual(homo_energy, -0.28830940)
        self.assertAlmostEqual(gap, 0.30767010)

        self.assertEqual(homo_unit, Units.hartree)
        self.assertEqual(lumo_unit, Units.hartree)
        self.assertEqual(gap_unit, Units.hartree)
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
        self.assertEqual(token.atomList()[0][2].value(), 1.091176 )
        self.assertEqual(token.atomList()[0][2].unit(), Units.angstrom)

        self.assertEqual(token.atomList()[8][0][0], "C4")
        self.assertEqual(token.atomList()[8][0][1], "2")
        self.assertEqual(token.atomList()[8][1][0], "C4")
        self.assertEqual(token.atomList()[8][1][1], "1")
        self.assertEqual(token.atomList()[8][2].value(), 1.460430)
        self.assertEqual(token.atomList()[8][2].unit(), Units.angstrom)

        # <<fold
    def testSymmetryToken(self): # fold>>
        data = FileSnippets.symmetry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SymmetryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(token.generators(), ["Z"]) 

        # <<fold
    def testSymmetryToken2(self): # fold>>
        data = FileSnippets.symmetry2()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SymmetryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+13)

        self.assertEqual(token.generators(), ["YZ", "X", "Y", "XYZ"]) 

        # <<fold
    def testSymmetryToken3(self): # fold>>
        data = FileSnippets.symmetry3()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SymmetryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+5)

        self.assertEqual(token.generators(), []) 

        # <<fold
    def testSymmetryToken4(self): # fold>>
        data = FileSnippets.symmetry4()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SymmetryToken.match(reader)
        
        self.assertEqual(token.__class__, Tokens.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(token.generators(), ["Z","XY"]) 

        # <<fold
    def testResponseHeaderToken(self): # fold>>
        data = FileSnippets.responseHeader()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.ResponseHeaderToken.match(reader)
        self.assertEqual(token.__class__, Tokens.ResponseHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+2)
        
    # <<fold
    def testFirstHyperpolarizabilityComponentToken(self): # fold>>
        data = FileSnippets.firstHyperpolarizability()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FirstHyperpolarizabilityComponentToken.match(reader)
        self.assertEqual(token.__class__, Tokens.FirstHyperpolarizabilityComponentToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertAlmostEqual(token.BFreq().value(), 0.0)
        self.assertAlmostEqual(token.CFreq().value(), 0.0)
        self.assertEqual(token.components(), ("X", "Y", "Z"))
        self.assertAlmostEqual(token.beta().value(),  -156.24941780)
        self.assertEqual(token.refersTo(), None)
        
    # <<fold
    def testFirstHyperpolarizabilityComponentToken1(self): # fold>>
        data = FileSnippets.firstHyperpolarizability1()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FirstHyperpolarizabilityComponentToken.match(reader)
        self.assertEqual(token.__class__, Tokens.FirstHyperpolarizabilityComponentToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertAlmostEqual(token.BFreq().value(), 0.123456)
        self.assertAlmostEqual(token.CFreq().value(), 0.654321)
        self.assertEqual(token.components(), ("X", "Y", "Z"))
        self.assertEqual(token.beta(), None)
        self.assertEqual(token.refersTo(), ("Z","Y","X"))
        
    # <<fold
    def testFirstHyperpolarizabilityComponentToken2(self): # fold>>
        data = FileSnippets.firstHyperpolarizability2()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.FirstHyperpolarizabilityComponentToken.match(reader)
        self.assertEqual(token.__class__, Tokens.FirstHyperpolarizabilityComponentToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertAlmostEqual(token.BFreq().value(), 0.065625)
        self.assertAlmostEqual(token.CFreq().value(), 0.000000)
        self.assertEqual(token.components(), ("X", "X", "X"))
        self.assertEqual(token.beta().value(), -101924.71581970)
        
    # <<fold
    def testSecondHyperpolarizabilityToken(self): # fold>>
        data = FileSnippets.secondHyperpolarizability()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SecondHyperpolarizabilityToken.match(reader)
        self.assertEqual(token.__class__, Tokens.SecondHyperpolarizabilityToken)
        self.assertEqual(reader.currentPos(), start_pos+30)
        
        self.assertAlmostEqual(token.BFreq().value(), 0.065625)
        self.assertAlmostEqual(token.CFreq().value(), 0.065625)
        self.assertAlmostEqual(token.DFreq().value(), 0.065625)

        
        self.assertAlmostEqual(token.gamma("X","X","X","X").value(),    355984.7821)
        self.assertAlmostEqual(token.gamma("X","X","Y","Y").value(),     28235.7103)
        self.assertAlmostEqual(token.gamma("X","Y","Y","X").value(),     28235.7103)
        self.assertAlmostEqual(token.gamma("X","Y","X","Y").value(),     28235.7103)
        self.assertAlmostEqual(token.gamma("X","X","Z","Z").value(),    117076.0321)
        self.assertAlmostEqual(token.gamma("X","Z","Z","X").value(),    117076.0321)
        self.assertAlmostEqual(token.gamma("X","Z","X","Z").value(),    117076.0321)
        self.assertAlmostEqual(token.gamma("Y","Y","X","X").value(),      7215.4984)
        self.assertAlmostEqual(token.gamma("Y","X","X","Y").value(),      7215.4984)
        self.assertAlmostEqual(token.gamma("Y","X","Y","X").value(),      7215.4984)
        self.assertAlmostEqual(token.gamma("Y","Y","Y","Y").value(),     15106.6644)
        self.assertAlmostEqual(token.gamma("Y","Y","Z","Z").value(),      7136.0750)
        self.assertAlmostEqual(token.gamma("Y","Z","Z","Y").value(),      7136.0750)
        self.assertAlmostEqual(token.gamma("Y","Z","Y","Z").value(),      7136.0750)
        self.assertAlmostEqual(token.gamma("Z","Z","X","X").value(),     41884.7566)
        self.assertAlmostEqual(token.gamma("Z","X","X","Z").value(),     41884.7566)
        self.assertAlmostEqual(token.gamma("Z","X","Z","X").value(),     41884.7566)
        self.assertAlmostEqual(token.gamma("Z","Z","Y","Y").value(),     12288.9233)
        self.assertAlmostEqual(token.gamma("Z","Y","Y","Z").value(),     12288.9233)
        self.assertAlmostEqual(token.gamma("Z","Y","Z","Y").value(),     12288.9233)
        self.assertAlmostEqual(token.gamma("Z","Z","Z","Z").value(),     42727.4395)

    # <<fold
    def testSecondHyperpolarizabilityToken2(self): # fold>>
        data = FileSnippets.secondHyperpolarizability2()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SecondHyperpolarizabilityToken.match(reader)
        self.assertEqual(token.__class__, Tokens.SecondHyperpolarizabilityToken)
        self.assertEqual(reader.currentPos(), start_pos+9)
        
        self.assertAlmostEqual(token.BFreq().value(), 0.0)
        self.assertAlmostEqual(token.CFreq().value(), 0.0)
        self.assertAlmostEqual(token.DFreq().value(), 0.0)

        self.assertAlmostEqual(token.gamma("X","X","X","X").value(), 402408.9623)
        self.assertEqual(token.gamma("X","X","Y","Y"),     None)
        self.assertEqual(token.gamma("X","Y","Y","X"),     None)
        self.assertEqual(token.gamma("X","Y","X","Y"),     None)
        self.assertEqual(token.gamma("X","X","Z","Z"),     None)
        self.assertEqual(token.gamma("X","Z","Z","X"),     None)
        self.assertEqual(token.gamma("X","Z","X","Z"),     None)
        self.assertEqual(token.gamma("Y","Y","X","X"),     None)
        self.assertEqual(token.gamma("Y","X","X","Y"),     None)
        self.assertEqual(token.gamma("Y","X","Y","X"),     None)
        self.assertEqual(token.gamma("Y","Y","Y","Y"),     None)
        self.assertEqual(token.gamma("Y","Y","Z","Z"),     None)
        self.assertEqual(token.gamma("Y","Z","Z","Y"),     None)
        self.assertEqual(token.gamma("Y","Z","Y","Z"),     None)
        self.assertEqual(token.gamma("Z","Z","X","X"),     None)
        self.assertEqual(token.gamma("Z","X","X","Z"),     None)
        self.assertEqual(token.gamma("Z","X","Z","X"),     None)
        self.assertEqual(token.gamma("Z","Z","Y","Y"),     None)
        self.assertEqual(token.gamma("Z","Y","Y","Z"),     None)
        self.assertEqual(token.gamma("Z","Y","Z","Y"),     None)
        self.assertEqual(token.gamma("Z","Z","Z","Z"),     None)

    # <<fold
    def testLinearResponseToken(self): # fold>>
        data = FileSnippets.linearResponse()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.LinearResponseToken.match(reader)
        self.assertEqual(token.__class__, Tokens.LinearResponseToken)
        self.assertEqual(reader.currentPos(), start_pos+6)
        
        self.assertAlmostEqual(token.AFreq().value(), 0.123456)
        self.assertAlmostEqual(token.BFreq().value(), 0.654321)

        self.assertAlmostEqual(token.alpha().value(), 125.676650646855)
        self.assertEqual(token.alpha().unit(), Units.alpha_au)
        self.assertEqual(token.components(), ["X","X"])
    # <<fold
    def testSevereErrorToken(self): # fold>>
        data = FileSnippets.severeError()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SevereErrorToken.match(reader)
        self.assertEqual(token.__class__, Tokens.SevereErrorToken)
        self.assertEqual(reader.currentPos(), start_pos+5)
        self.assertEqual(token.reason(), "*** FNDGEO *** No acceptable step found.")

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
    def testBondLengthsTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.BondLengthsToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testSymmetryTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SymmetryToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

        # <<fold
    def testResponseHeaderTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.ResponseHeaderToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

    # <<fold
    def notestFirstHyperpolarizabilityTokenNotMatching(self): # fold>>
        self.assertEqual(0,1)
    # <<fold
    def testSecondHyperpolarizabilityTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SecondHyperpolarizabilityToken.match(reader)
        
        self.assertEqual(token, None)
        self.assertEqual(reader.currentPos(), start_pos)

    # <<fold
    def testSevereErrorTokenNotMatching(self): # fold>>
        data = FileSnippets.optimizationNextGeometry()

        writeToTestFile(data)
        
        reader = FileReader.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = Tokens.SevereErrorToken.match(reader)
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
    
