# @author Stefano Borini
import os 
import sys
import unittest

from wavemol.parsers.tests.dalton import filesnippets
from wavemol.parsers.dalton import tokentypes
from wavemol.core import io
from wavemol.core import units

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
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.FileHeaderToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.FileHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testCenterOfMassToken(self): # fold>>
        data = filesnippets.centerOfMass()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.CenterOfMassToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.CenterOfMassToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
        self.assertEqual(token.centerOfMass().__class__, units.Quantity)
        self.assertEqual(len(token.centerOfMass()), 3)
        self.assertAlmostEqual(token.centerOfMass()[0], 0.000000 * units.bohr)
        self.assertAlmostEqual(token.centerOfMass()[1], 1.000000 * units.bohr)
        self.assertAlmostEqual(token.centerOfMass()[2], 1.223609 * units.bohr)
        
         
         # <<fold
    def testTotalMassToken(self): # fold>>
        data = filesnippets.totalMass()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.TotalMassToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.TotalMassToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertEqual(token.totalMass().__class__, units.Quantity )
        self.assertEqual(token.totalMass(), 30.010565 * units.dalton)
    # <<fold
    def testIsotopicMassesToken(self): # fold>>
        data = filesnippets.isotopicMasses()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.IsotopicMassesToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.IsotopicMassesToken)
        self.assertEqual(reader.currentPos(), start_pos+8)
       
        atom_list = token.atomList()
        self.assertEqual(type(atom_list), type([]))
        self.assertEqual(len(atom_list), 4)

        self.assertEqual(atom_list[0][0], "O1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2].__class__, units.Quantity)
        self.assertEqual(atom_list[0][2], 15.994915 * units.dalton)

        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2].__class__, units.Quantity )
        self.assertEqual(atom_list[1][2], 1.007825 * units.dalton)

        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2].__class__, units.Quantity )
        self.assertEqual(atom_list[2][2], 1.007825 * units.dalton)

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, units.Quantity )
        self.assertEqual(atom_list[3][2], 12.0000 * units.dalton)
        
        # <<fold
    def testMomentsOfInertiaToken(self): # fold>>
        data = filesnippets.momentsOfInertia()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.MomentsOfInertiaToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.MomentsOfInertiaToken)
        self.assertEqual(reader.currentPos(), start_pos+7)

        moments = token.momentsOfInertia()
        self.assertEqual(moments.__class__, list)

        self.assertEqual(moments[0], 1.747844 * units.dalton * units.angstrom * units.angstrom)
        self.assertEqual(moments[1], 13.208584 * units.dalton * units.angstrom * units.angstrom)
        self.assertEqual(moments[2], 14.956428 * units.dalton * units.angstrom * units.angstrom)

        principal_axes = token.principalAxes()
        self.assertEqual(principal_axes.__class__, list)
        for i,j in [(0,0), (0,1), (1,0), (1,2), (2,1), (2,2)]:
            self.assertEqual(principal_axes[i][j], 0.000000 * units.angstrom)
        for i,j in [(0,2), (1,1), (0,2)]:
            self.assertEqual(principal_axes[i][j], 1.000000 * units.angstrom)

        # <<fold
    def testCartesianCoordinatesToken(self): # fold>>
        data = filesnippets.cartesianCoordinates()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.CartesianCoordinatesToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.CartesianCoordinatesToken)
        self.assertEqual(reader.currentPos(), start_pos+22)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 4)

        self.assertEqual(atom_list[0][0], "O1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2].__class__, units.Quantity)
        self.assertEqual(atom_list[0][2][0], 0.0000000000 * units.bohr)
        self.assertEqual(atom_list[0][2][1], 0.0000000000 * units.bohr)
        self.assertEqual(atom_list[0][2][2], 0.3000000000 * units.bohr)
   
        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[0][2].__class__, units.Quantity)
        self.assertEqual(atom_list[1][2][0], 0.0000000000 * units.bohr)
        self.assertEqual(atom_list[1][2][1],-1.7597098488 * units.bohr)
        self.assertEqual(atom_list[1][2][2],3.3775957364  * units.bohr)


        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2].__class__, units.Quantity)
        self.assertEqual(atom_list[2][2][0], 0.0000000000 * units.bohr)
        self.assertEqual(atom_list[2][2][1], 1.7597098488 * units.bohr)
        self.assertEqual(atom_list[2][2][2], 3.3775957364 * units.bohr)

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, units.Quantity)
        self.assertEqual(atom_list[3][2][0],0.0000000000 * units.bohr)
        self.assertEqual(atom_list[3][2][1],0.0000000000 * units.bohr)
        self.assertEqual(atom_list[3][2][2],2.3051919000 * units.bohr)

        # <<fold
    def testCartesianCoordinatesToken2(self): # fold>>
        data = filesnippets.cartesianCoordinates2()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.CartesianCoordinatesToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.CartesianCoordinatesToken)
        self.assertEqual(reader.currentPos(), start_pos+53)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 12)

        # <<fold
    def testCartesianCoordinatesToken3(self): # fold>>
        data = filesnippets.cartesianCoordinates3()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.CartesianCoordinatesToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.CartesianCoordinatesToken)
        self.assertEqual(reader.currentPos(), start_pos+181)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 44)

        # <<fold
    def testEndOfOptimizationHeaderToken(self): # fold>>
        data = filesnippets.endOfOptimizationHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.EndOfOptimizationHeaderToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.EndOfOptimizationHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        # <<fold
    def testFinalGeometryEnergyToken(self): # fold>>
        data = filesnippets.finalGeometryEnergy()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.FinalGeometryEnergyToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.FinalGeometryEnergyToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
       
        energy = token.energy()
        self.assertEqual(energy.__class__, units.Quantity)
        self.assertEqual(energy,-113.984888 * units.hartree)
        
        # <<fold
    def testGeometryConvergenceNumIterationsToken(self): # fold>>
        data = filesnippets.geometryConvergenceNumIterations()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.GeometryConvergenceNumIterationsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.GeometryConvergenceNumIterationsToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
       
        iterations = token.iterations()
        self.assertEqual(type(iterations), type(1))
        self.assertEqual(iterations,8)
        
        # <<fold
    def testOptimizationNextGeometryToken(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptimizationNextGeometryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.OptimizationNextGeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+8)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 4)

        self.assertEqual(atom_list[0][0], "O1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2].__class__, units.Quantity)
        self.assertEqual(atom_list[0][2][0], 0.0000000000*units.bohr)
        self.assertEqual(atom_list[0][2][1], 0.0000000000*units.bohr)
        self.assertEqual(atom_list[0][2][2], 0.0680928675*units.bohr)
   
        self.assertEqual(atom_list[1][0], "H1")
        self.assertEqual(atom_list[1][1], "1")
        self.assertEqual(atom_list[1][2].__class__, units.Quantity)
        self.assertEqual(atom_list[1][2][0], 0.0000000000*units.bohr)
        self.assertEqual(atom_list[1][2][1], -1.7554324515*units.bohr)
        self.assertEqual(atom_list[1][2][2], 3.4700805319*units.bohr)

        self.assertEqual(atom_list[2][0], "H1")
        self.assertEqual(atom_list[2][1], "2")
        self.assertEqual(atom_list[2][2].__class__, units.Quantity)
        self.assertEqual(atom_list[2][2][0], 0.0000000000*units.bohr)
        self.assertEqual(atom_list[2][2][1], 1.7554324515*units.bohr)
        self.assertEqual(atom_list[2][2][2], 3.4700805319*units.bohr)

        self.assertEqual(atom_list[3][0], "C1")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2].__class__, units.Quantity)
        self.assertEqual(atom_list[3][2][0], 0.0000000000*units.bohr)
        self.assertEqual(atom_list[3][2][1], 0.0000000000*units.bohr)
        self.assertEqual(atom_list[3][2][2], 2.3521294415*units.bohr)

        # <<fold
    def testOptimizationInfoToken(self): # fold>>
        data = filesnippets.optimizationInfo()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptimizationInfoToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.OptimizationInfoToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(token.iteration(), 0)
        self.assertEqual(token.endOfOptimization(), False)
        self.assertEqual(token.energy().__class__, units.Quantity)
        self.assertEqual(token.energy(), -113.932636 * units.hartree)
        self.assertEqual(token.energyChange(), None)
        self.assertEqual(token.gradientNorm().__class__, units.Quantity)
        self.assertEqual(token.gradientNorm(), 0.567825 * units.unknown)
        self.assertEqual(token.stepNorm().__class__, units.Quantity)
        self.assertEqual(token.stepNorm(), 0.487002 * units.unknown)
        self.assertEqual(token.trustRadius().__class__, units.Quantity)
        self.assertEqual(token.trustRadius(), 0.500000*units.unknown)
        self.assertEqual(token.totalHessianIndex(), 0)

        # <<fold
    def testOptimizationInfoToken2(self): # fold>>
        data = filesnippets.optimizationInfo2()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptimizationInfoToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.OptimizationInfoToken)
        self.assertEqual(reader.currentPos(), start_pos+11)

        self.assertEqual(token.iteration(), 1)
        self.assertEqual(token.endOfOptimization(), True)
        self.assertEqual(token.energy(), -113.984495 * units.hartree)
        self.assertEqual(token.energyChange(), -0.051859 * units.hartree)
        self.assertEqual(token.gradientNorm(), 0.030306 * units.unknown)
        self.assertEqual(token.stepNorm(), 0.030552 * units.unknown)
        self.assertEqual(token.trustRadius(), 0.584403 * units.unknown)
        self.assertEqual(token.totalHessianIndex(), 0)

        # <<fold
    def testNormalModesEigenvaluesToken(self): # fold>>
        data = filesnippets.normalModesEigenvalues()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.NormalModesEigenvaluesToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.NormalModesEigenvaluesToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(len(token.values()), 6)
        for index, correct_value in enumerate([1.279649E-42,1.279649E-42,4.094095E-04,9.790871E-44,9.790871E-44, -1.212226E-21]):
            self.assertAlmostEqual(token.values()[index], correct_value * units.unknown)

        # <<fold
    def testAtomsAndBasisSetsToken(self): # fold>>
        data = filesnippets.atomsAndBasisSetsTable()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.AtomsAndBasisSetsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.AtomsAndBasisSetsToken)
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
        data = filesnippets.atomsAndBasisSetsTable2()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.AtomsAndBasisSetsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.AtomsAndBasisSetsToken)
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
        data = filesnippets.atomsAndBasisSetsTable3()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.AtomsAndBasisSetsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.AtomsAndBasisSetsToken)

        # <<fold
    def testFinalGeometryToken(self): # fold>>
        data = filesnippets.finalGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.FinalGeometryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.FinalGeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+14)

        atom_list = token.atomList()

        self.assertEqual(len(atom_list), 10)

        self.assertEqual(atom_list[0][0], "H1")
        self.assertEqual(atom_list[0][1], "")
        self.assertEqual(atom_list[0][2][0], 0.0000002307 * units.bohr)
        self.assertEqual(atom_list[0][2][1], -0.0431166985 * units.bohr)
        self.assertEqual(atom_list[0][2][2], -0.0202403617 * units.bohr)
   
        self.assertEqual(atom_list[1][0], "H2")
        self.assertEqual(atom_list[1][1], "")
        self.assertEqual(atom_list[1][2][0], 0.0000001751 * units.bohr)
        self.assertEqual(atom_list[1][2][1], 1.6729220095 * units.bohr)
        self.assertEqual(atom_list[1][2][2], -3.0984614789 * units.bohr)

        self.assertEqual(atom_list[2][0], "H3")
        self.assertEqual(atom_list[2][1], "")
        self.assertEqual(atom_list[2][2][0], -0.0000000621 * units.bohr)
        self.assertEqual(atom_list[2][2][1], 3.9834654382 * units.bohr)
        self.assertEqual(atom_list[2][2][2], 2.2591198806 * units.bohr)

        self.assertEqual(atom_list[3][0], "H4")
        self.assertEqual(atom_list[3][1], "")
        self.assertEqual(atom_list[3][2][0], -0.0000004152 * units.bohr)
        self.assertEqual(atom_list[3][2][1], 6.3971763363 * units.bohr)
        self.assertEqual(atom_list[3][2][2], -3.1312282876 * units.bohr)

        self.assertEqual(atom_list[4][0], "H5")
        self.assertEqual(atom_list[4][1], "")
        self.assertEqual(atom_list[4][2][0],0.0000000584 * units.bohr)
        self.assertEqual(atom_list[4][2][1],8.7077203406 * units.bohr)
        self.assertEqual(atom_list[4][2][2],2.2263528516 * units.bohr)

        self.assertEqual(atom_list[5][0], "H6")
        self.assertEqual(atom_list[5][1], "")
        self.assertEqual(atom_list[5][2][0], 0.0000011485 * units.bohr)
        self.assertEqual(atom_list[5][2][1], 10.4237584759 * units.bohr)
        self.assertEqual(atom_list[5][2][2], -0.8518686398 * units.bohr)

        self.assertEqual(atom_list[6][0], "C1")
        self.assertEqual(atom_list[6][1], "")
        self.assertEqual(atom_list[6][2][0], 0.0000002040 * units.bohr)
        self.assertEqual(atom_list[6][2][1], 1.7527241877 * units.bohr)
        self.assertEqual(atom_list[6][2][2], -1.0336061328 * units.bohr)

        self.assertEqual(atom_list[7][0], "C2")
        self.assertEqual(atom_list[7][1], "")
        self.assertEqual(atom_list[7][2][0], -0.0000000301 * units.bohr)
        self.assertEqual(atom_list[7][2][1], 3.9601114154 * units.bohr)
        self.assertEqual(atom_list[7][2][2], 0.1889860925 * units.bohr)

        self.assertEqual(atom_list[8][0], "C3")
        self.assertEqual(atom_list[8][1], "")
        self.assertEqual(atom_list[8][2][0], -0.0000005431 * units.bohr)
        self.assertEqual(atom_list[8][2][1], 6.4205305038 * units.bohr)
        self.assertEqual(atom_list[8][2][2], -1.0610944968 * units.bohr)

        self.assertEqual(atom_list[9][0], "C4")
        self.assertEqual(atom_list[9][1], "")
        self.assertEqual(atom_list[9][2][0], -0.0000007662 * units.bohr)
        self.assertEqual(atom_list[9][2][1], 8.6279178237 * units.bohr)
        self.assertEqual(atom_list[9][2][2], 0.1614975188 * units.bohr)

        # <<fold
    def testDipoleMomentToken(self): # fold>>
        data = filesnippets.dipoleMoment()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.DipoleMomentToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.DipoleMomentToken)
        self.assertEqual(reader.currentPos(), start_pos+4)

        dipole = token.dipole()
        self.assertEqual(dipole, 3.1415927 * units.debye)

        # <<fold
    def testDipoleMomentComponents(self): # fold>>
        data = filesnippets.dipoleMomentComponents()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.DipoleMomentComponentsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.DipoleMomentComponentsToken)
        self.assertEqual(reader.currentPos(), start_pos+8)
        
        dipole = token.dipole()
        self.assertEqual(dipole[0], 3.14159270 * units.debye)
        self.assertEqual(dipole[1], -1.23456789 * units.debye)
        self.assertEqual(dipole[2], 9.87654321 * units.debye)
        # <<fold
    def testHOMOLUMOSeparationToken(self): # fold>>
        data = filesnippets.HomoLumoSeparation()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.HOMOLUMOSeparationToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.HOMOLUMOSeparationToken)
        self.assertEqual(reader.currentPos(), start_pos+4)

        lumo_energy = token.LUMOEnergy()
        homo_energy = token.HOMOEnergy()
        lumo_symmetry = token.LUMOSymmetry()
        homo_symmetry = token.HOMOSymmetry()

        gap = token.gap()

        self.assertAlmostEqual(lumo_energy, 0.01936070 * units.hartree)
        self.assertEqual(lumo_symmetry, 1)
        self.assertEqual(homo_symmetry, 1)
        self.assertAlmostEqual(homo_energy, -0.28830940 * units.hartree)
        self.assertAlmostEqual(gap, 0.30767010 * units.hartree)

        # <<fold
    def testBondLengthsToken(self): # fold>>
        data = filesnippets.bondLengths()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.BondLengthsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.BondLengthsToken)
        self.assertEqual(reader.currentPos(), start_pos+15)

        self.assertEqual(len(token.atomList()), 9)

        self.assertEqual(token.atomList()[0][0][0], "C2")
        self.assertEqual(token.atomList()[0][0][1], "1")
        self.assertEqual(token.atomList()[0][1][0], "H1")
        self.assertEqual(token.atomList()[0][1][1], "1")
        self.assertEqual(token.atomList()[0][2], 1.091176 * units.angstrom)

        self.assertEqual(token.atomList()[8][0][0], "C4")
        self.assertEqual(token.atomList()[8][0][1], "2")
        self.assertEqual(token.atomList()[8][1][0], "C4")
        self.assertEqual(token.atomList()[8][1][1], "1")
        self.assertEqual(token.atomList()[8][2], 1.460430 * units.angstrom)

        # <<fold
    def testSymmetryToken(self): # fold>>
        data = filesnippets.symmetry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SymmetryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(token.generators(), ["Z"]) 

        # <<fold
    def testSymmetryToken2(self): # fold>>
        data = filesnippets.symmetry2()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SymmetryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+13)

        self.assertEqual(token.generators(), ["YZ", "X", "Y", "XYZ"]) 

        # <<fold
    def testSymmetryToken3(self): # fold>>
        data = filesnippets.symmetry3()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SymmetryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+5)

        self.assertEqual(token.generators(), []) 

        # <<fold
    def testSymmetryToken4(self): # fold>>
        data = filesnippets.symmetry4()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SymmetryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.SymmetryToken)
        self.assertEqual(reader.currentPos(), start_pos+10)

        self.assertEqual(token.generators(), ["Z","XY"]) 

        # <<fold
    def testResponseHeaderToken(self): # fold>>
        data = filesnippets.responseHeader()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.ResponseHeaderToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.ResponseHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+2)
        
    # <<fold
    def testFirstHyperpolarizabilityComponentToken(self): # fold>>
        data = filesnippets.firstHyperpolarizability()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.FirstHyperpolarizabilityComponentToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.FirstHyperpolarizabilityComponentToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertAlmostEqual(token.BFreq(), 0.0 * units.hartree)
        self.assertAlmostEqual(token.CFreq(), 0.0 * units.hartree)
        self.assertEqual(token.components(), ("X", "Y", "Z"))
        self.assertAlmostEqual(token.beta(),  -156.24941780 * units.atomic_unit_of_1st_hyperpolarizability)
        self.assertEqual(token.refersTo(), None)
        
    # <<fold
    def testFirstHyperpolarizabilityComponentToken1(self): # fold>>
        data = filesnippets.firstHyperpolarizability1()

        writeToTestFile(data)
       
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.FirstHyperpolarizabilityComponentToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.FirstHyperpolarizabilityComponentToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertAlmostEqual(token.BFreq(), 0.123456 * units.hartree)
        self.assertAlmostEqual(token.CFreq(), 0.654321 * units.hartree)
        self.assertEqual(token.components(), ("X", "Y", "Z"))
        self.assertEqual(token.beta(), None)
        self.assertEqual(token.refersTo(), ("Z","Y","X"))
        
    # <<fold
    def testFirstHyperpolarizabilityComponentToken2(self): # fold>>
        data = filesnippets.firstHyperpolarizability2()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.FirstHyperpolarizabilityComponentToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.FirstHyperpolarizabilityComponentToken)
        self.assertEqual(reader.currentPos(), start_pos+1)

        self.assertAlmostEqual(token.BFreq(), 0.065625 * units.hartree)
        self.assertAlmostEqual(token.CFreq(), 0.000000 * units.hartree)
        self.assertEqual(token.components(), ("X", "X", "X"))
        self.assertEqual(token.beta(), -101924.71581970 * units.atomic_unit_of_1st_hyperpolarizability)
        
    # <<fold
    def testSecondHyperpolarizabilityToken(self): # fold>>
        data = filesnippets.secondHyperpolarizability()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SecondHyperpolarizabilityToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.SecondHyperpolarizabilityToken)
        self.assertEqual(reader.currentPos(), start_pos+30)
        
        self.assertAlmostEqual(token.BFreq(), 0.065625 * units.hartree)
        self.assertAlmostEqual(token.CFreq(), 0.065625 * units.hartree)
        self.assertAlmostEqual(token.DFreq(), 0.065625 * units.hartree)

        
        self.assertAlmostEqual(token.gamma("X","X","X","X"),    355984.7821*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("X","X","Y","Y"),     28235.7103*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("X","Y","Y","X"),     28235.7103*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("X","Y","X","Y"),     28235.7103*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("X","X","Z","Z"),    117076.0321*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("X","Z","Z","X"),    117076.0321*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("X","Z","X","Z"),    117076.0321*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","Y","X","X"),      7215.4984*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","X","X","Y"),      7215.4984*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","X","Y","X"),      7215.4984*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","Y","Y","Y"),     15106.6644*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","Y","Z","Z"),      7136.0750*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","Z","Z","Y"),      7136.0750*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Y","Z","Y","Z"),      7136.0750*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","Z","X","X"),     41884.7566*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","X","X","Z"),     41884.7566*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","X","Z","X"),     41884.7566*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","Z","Y","Y"),     12288.9233*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","Y","Y","Z"),     12288.9233*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","Y","Z","Y"),     12288.9233*units.atomic_unit_of_2nd_hyperpolarizability)
        self.assertAlmostEqual(token.gamma("Z","Z","Z","Z"),     42727.4395*units.atomic_unit_of_2nd_hyperpolarizability)

    # <<fold
    def testSecondHyperpolarizabilityToken2(self): # fold>>
        data = filesnippets.secondHyperpolarizability2()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SecondHyperpolarizabilityToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.SecondHyperpolarizabilityToken)
        self.assertEqual(reader.currentPos(), start_pos+9)
        
        self.assertAlmostEqual(token.BFreq(), 0.0 * units.hartree)
        self.assertAlmostEqual(token.CFreq(), 0.0 * units.hartree)
        self.assertAlmostEqual(token.DFreq(), 0.0 * units.hartree)

        self.assertAlmostEqual(token.gamma("X","X","X","X"), 402408.9623 * units.atomic_unit_of_2nd_hyperpolarizability)
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
        data = filesnippets.linearResponse()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.LinearResponseToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.LinearResponseToken)
        self.assertEqual(reader.currentPos(), start_pos+6)
        
        self.assertAlmostEqual(token.AFreq(), 0.123456* units.hartree)
        self.assertAlmostEqual(token.BFreq(), 0.654321 * units.hartree)

        self.assertAlmostEqual(token.alpha(), 125.676650646855 * units.atomic_unit_of_electric_polarizability)
        self.assertEqual(token.components(), ["X","X"])
    # <<fold
    def testSevereErrorToken(self): # fold>>
        data = filesnippets.severeError()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SevereErrorToken.match(reader, [])
        self.assertEqual(token.__class__, tokentypes.SevereErrorToken)
        self.assertEqual(reader.currentPos(), start_pos+5)
        self.assertEqual(token.reason(), "*** FNDGEO *** No acceptable step found.")

    # <<fold
        
    def testFileHeaderTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile("\n"+data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.FileHeaderToken.match(reader, [])
        
        self.assertEqual(token, None)
        # <<fold
    def testCenterOfMassTokenNotMatching(self): # fold>>
        data = filesnippets.centerOfMass()
        writeToTestFile("\n"+data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.CenterOfMassToken.match(reader, [])
        
        self.assertEqual(token, None)
         # <<fold
    def testIsotopicMassesTokenNotMatching(self): # fold>>
        data = filesnippets.isotopicMasses()
        writeToTestFile("\n"+data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.IsotopicMassesToken.match(reader, [])
        
        self.assertEqual(token, None)
        # <<fold
    def testTotalMassTokenNotMatching(self): # fold>>
        data = filesnippets.totalMass()
        writeToTestFile("\n"+data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.TotalMassToken.match(reader, [])
        
        self.assertEqual(token, None)
        # <<fold 
    def testMomentsOfInertiaTokenNotMatching(self): # fold>>
        data = filesnippets.momentsOfInertia()
        writeToTestFile("\n"+data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.MomentsOfInertiaToken.match(reader, [])
        
        self.assertEqual(token, None)
        # <<fold
    def testCartesianCoordinatesTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.CartesianCoordinatesToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testEndOfOptimizationHeaderTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.EndOfOptimizationHeaderToken.match(reader, [])
        
        self.assertEqual(token, None)
        # <<fold
    def testFinalGeometryEnergyTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.FinalGeometryEnergyToken.match(reader, [])
        
        self.assertEqual(token, None)
        # <<fold
    def testGeometryConvergenceNumIterationsTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.GeometryConvergenceNumIterationsToken.match(reader, [])
        
        self.assertEqual(token, None)
       
        # <<fold
    def testOptimizationNextGeometryTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.OptimizationNextGeometryToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testOptimizationInfoTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.OptimizationInfoToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testNormalModesEigenvaluesTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.NormalModesEigenvaluesToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testAtomsAndBasisSetsTokenNotMatching(self): # fold>>
        data = filesnippets.fileHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.AtomsAndBasisSetsToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testFinalGeometryTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.FinalGeometryToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testDipoleMomentTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.DipoleMomentToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testDipoleMomentComponentsTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.DipoleMomentComponentsToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testHOMOLUMOSeparationTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.HOMOLUMOSeparationToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testBondLengthsTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.BondLengthsToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testSymmetryTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.SymmetryToken.match(reader, [])
        
        self.assertEqual(token, None)

        # <<fold
    def testResponseHeaderTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.ResponseHeaderToken.match(reader, [])
        
        self.assertEqual(token, None)

    # <<fold
    def notestFirstHyperpolarizabilityTokenNotMatching(self): # fold>>
        self.assertEqual(0,1)
    # <<fold
    def testSecondHyperpolarizabilityTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.SecondHyperpolarizabilityToken.match(reader, [])
        
        self.assertEqual(token, None)

    # <<fold
    def testSevereErrorTokenNotMatching(self): # fold>>
        data = filesnippets.optimizationNextGeometry()

        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        token = tokentypes.SevereErrorToken.match(reader, [])
        self.assertEqual(token, None)

    # <<fold

    def testTryReadColumnHeader(self): # fold>>
        self.assertEqual(tokentypes._tryReadColumnHeader(""), None)
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5"), [5])
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6"), [5,6])
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6  "), [5,6])
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6 boo "), None)
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6 Column 7"), [5,6,7])
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6 Column 7 Column 8"), [5,6,7,8])
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6 Column 7 Column 8 Column 9"), [5,6,7,8,9])
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column 5 Column 6 Column 7 Column x"), None)
        self.assertEqual(tokentypes._tryReadColumnHeader(" Column x Column 6 Column 7 Column x"), None)
        # <<fold
    def testTryReadRowValues(self): # fold>>
        self.assertEqual(tokentypes._tryReadRowValues(""), None)

        t = tokentypes._tryReadRowValues("  1     1.279649E-02   5.279649E-02   4.094095E-04   3.790871E-04 ")
        self.assertNotEqual(t, None)
        self.assertEqual(len(t), 2)
        index, values = t
        self.assertEqual(index, 1)
        self.assertEqual(len(values), 4)
        self.assertAlmostEqual(values[0], 1.279649E-02)
        self.assertAlmostEqual(values[1], 5.279649E-02)
        self.assertAlmostEqual(values[2], 4.094095E-04)
        self.assertAlmostEqual(values[3], 3.790871E-04)
        
        t = tokentypes._tryReadRowValues("  1     1.279649E-02 x  5.279649E-02   4.094095E-04   3.790871E-04 ")
        self.assertEqual(t, None)

        t = tokentypes._tryReadRowValues("  1     1.279649E-02  ")
        self.assertNotEqual(t, None)
        self.assertEqual(len(t), 2)
        index, values = t
        self.assertEqual(index, 1)
        self.assertEqual(len(values), 1)
        self.assertAlmostEqual(values[0], 1.279649E-02)
        # <<fold
