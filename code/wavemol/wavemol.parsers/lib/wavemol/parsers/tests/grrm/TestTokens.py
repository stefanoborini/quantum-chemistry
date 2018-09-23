# @author Stefano Borini
import os
import sys
import unittest

from wavemol.parsers.grrm import tokentypes
from wavemol.core import io
from wavemol.core import units 

from . import filesnippets

def moduleDir():
    return os.path.dirname(__file__)

def testFilePath():
    return os.path.join(moduleDir(), "testfile-TestTokens")
def writeToTestFile(data):
    f = file(testFilePath(), "w")
    f.write(data)
    f.close()
    
class TestTokens(unittest.TestCase):
# the output file
    def testHeaderDissociatedToken(self):
        data = filesnippets.headerDissociated()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.HeaderDissociatedToken.match(reader,[])
        
        self.assertEqual(token.__class__, tokentypes.HeaderDissociatedToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
    def testHeaderEquilibriumToken(self):
        data = filesnippets.headerEquilibrium()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.HeaderEquilibriumToken.match(reader,[])
        
        self.assertEqual(token.__class__, tokentypes.HeaderEquilibriumToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
    def testHeaderTransitionToken(self):
        data = filesnippets.headerTransition()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.HeaderTransitionToken.match(reader,[])
        
        self.assertEqual(token.__class__, tokentypes.HeaderTransitionToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
    def testStructureHeaderToken(self):
        data = filesnippets.structureHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.StructureHeaderToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.StructureHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.type(), "DC")
        self.assertEqual(token.number(), 1)
        self.assertEqual(token.symmetry(), "C1")
        
    def testGeometryToken(self):
        data = filesnippets.geometry()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.GeometryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.GeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+9)
        self.assertEqual(len(token.atomList()), 9 )
        
    def testEnergyToken(self):
        data = filesnippets.energy()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.EnergyToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.EnergyToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertAlmostEqual(token.energy(), -153.869550889154 * units.hartree)
        
    def testSpinToken(self):
        data = filesnippets.spin()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SpinToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.SpinToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.spin(), 0.0 )
        
    def testZPVEToken(self):
        data = filesnippets.zpve()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.ZPVEToken.match(reader,[])
        
        self.assertEqual(token.__class__, tokentypes.ZPVEToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.zpve(), 0.074920061481 * units.hartree )
        
    def testNormalModesToken(self):
        data = filesnippets.normalModes()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.NormalModesToken.match(reader,[])
        
        self.assertEqual(token.__class__, tokentypes.NormalModesToken)
        self.assertEqual(reader.currentPos(), start_pos+5)
        self.assertEqual(len(token.eigenvalues()), 20 )
        
    def testConnectionToken(self):
        data = filesnippets.connection()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.ConnectionToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.ConnectionToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.first(), "0" )
        self.assertEqual(token.second(), "DC" )
    def testDissociationFragmentsToken(self):
        data = filesnippets.dissociationFragments()
        writeToTestFile(data)

        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.DissociationFragmentsToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.DissociationFragmentsToken)
        self.assertEqual(reader.currentPos(), start_pos+4)
        self.assertEqual(token.numFragments(), 2 )
        self.assertEqual(token.fragment(0), [1,2] )
        self.assertEqual(token.fragment(1), [3,4] )
        

# the input file
    def testCommandDirectiveToken(self):
        data = filesnippets.commandDirective()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.CommandDirectiveToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.CommandDirectiveToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.commandLine(), "grrm/RHF/6-31+G*")
        self.assertEqual(token.jobString(), "grrm")
        self.assertEqual(token.methodString(), "RHF")
        self.assertEqual(token.basisSetString(), "6-31+G*")
        
    def testInputGeometryToken(self):
        data = filesnippets.molecule()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.InputGeometryToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.InputGeometryToken)
        self.assertEqual(reader.currentPos(), start_pos+5)
        self.assertEqual(len(token.atomList()), 4)
        self.assertEqual(token.charge(), 0)
        self.assertEqual(token.spinMultiplicity(), 1)
        
    def testOptionsHeaderToken(self):
        data = filesnippets.optionsHeader()
        writeToTestFile(data)

        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptionsHeaderToken.match(reader, [])
        
        self.assertEqual(token.__class__, tokentypes.OptionsHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
    def testNRunOptionToken(self):
        data = filesnippets.nrunOption()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.NRunOptionToken.match(reader, [])
        
        self.assertEqual(token.__class__,tokentypes.NRunOptionToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.value(), 4)
        

# the TS IRC energy analysis

    def testOptimizationHeaderToken(self):
        data = filesnippets.optimizationHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptimizationHeaderToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.OptimizationHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
    def testOptimizationIterationToken(self):
        data = filesnippets.optimizationIteration()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptimizationIterationToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.OptimizationIterationToken)
        self.assertEqual(reader.currentPos(), start_pos+15)
    def testOptimizationFinalStructureToken(self):
        data = filesnippets.optimizationFinalStructure()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.OptimizationFinalStructureToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.OptimizationFinalStructureToken)
        self.assertEqual(reader.currentPos(), start_pos+8)
    def testNormalModesTSToken(self):
        data = filesnippets.normalModesTS()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.NormalModesTSToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.NormalModesTSToken)
        self.assertEqual(reader.currentPos(), start_pos+3)
        self.assertEqual(len(token.eigenvalues()), 6)
    def testMinimumPointFoundHeaderToken(self):
        data = filesnippets.minimumPointFoundHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.MinimumPointFoundHeaderToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.MinimumPointFoundHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
    def testInitialStructureToken(self):
        data = filesnippets.initialStructure()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.InitialStructureToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.InitialStructureToken)
        self.assertEqual(reader.currentPos(), start_pos+7)
        self.assertEqual(len(token.atomList()), 4)
        self.assertEqual(token.energy(), -113.698521354847 * units.hartree )
    def testIRCHeaderToken(self):
        data = filesnippets.ircHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.IRCHeaderToken.match(reader,[])
        
        self.assertEqual(token.__class__, tokentypes.IRCHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
    def testEnergyProfileToken(self):
        data = filesnippets.energyProfile()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.EnergyProfileToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.EnergyProfileToken)
        self.assertEqual(reader.currentPos(), start_pos+73)
    def testBackwardIRCHeaderToken(self):
        data = filesnippets.backwardIRCHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.BackwardIRCHeaderToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.BackwardIRCHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
    def testForwardIRCHeaderToken(self):
        data = filesnippets.forwardIRCHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.ForwardIRCHeaderToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.ForwardIRCHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
    def testIRCFollowingResultsToken(self):
        data = filesnippets.ircFollowingResults()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.IRCFollowingResultsToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.IRCFollowingResultsToken)
        self.assertEqual(reader.currentPos(), start_pos+3)
        self.assertEqual(token.forward()[0], "DC")
        self.assertEqual(token.forward()[1], 3)
        self.assertEqual(token.backward()[0], "EQ")
        self.assertEqual(token.backward()[1], 2)
    def testIRCStepToken(self):
        data = filesnippets.IRCStep()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.IRCStepToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.IRCStepToken)
        self.assertEqual(reader.currentPos(), start_pos+7)
        self.assertEqual(token.step(), 2)
        self.assertEqual(len(token.atomList()), 4)
        self.assertEqual(token.energy(), -113.615808262609 * units.hartree)
        self.assertEqual(token.spin(), 0.0 * units.hbar) 
    def testDCReachedToken(self):
        data = filesnippets.DCReached()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.DCReachedToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.DCReachedToken)
        self.assertEqual(reader.currentPos(), start_pos+8)
    def testEQWithinStepsizeHeaderToken(self):
        data = filesnippets.EQWithinStepsizeHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.EQWithinStepsizeHeaderToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.EQWithinStepsizeHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
    def testGradientVectorToken(self):
        data = filesnippets.gradientVector()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.GradientVectorToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.GradientVectorToken)
        self.assertEqual(reader.currentPos(), start_pos+14)
        self.assertEqual(len(token.vector()), 12 )
        self.assertEqual(token.vector()[1], -0.000000093893 * units.unknown) 
    def testSteepestDescentHeaderToken(self):
        data = filesnippets.steepestDescentHeader()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.SteepestDescentHeaderToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.SteepestDescentHeaderToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        
    def testDownhillWalkingResultToken(self):
        data = filesnippets.downhillWalkingResult()
        writeToTestFile(data)
        
        reader = io.FileReader(testFilePath())
        start_pos = reader.currentPos()
        token = tokentypes.DownhillWalkingResultToken.match(reader,[])
        self.assertEqual(token.__class__, tokentypes.DownhillWalkingResultToken)
        self.assertEqual(reader.currentPos(), start_pos+1)
        self.assertEqual(token.result()[0], "EQ")
        self.assertEqual(token.result()[1], 2)
        
        
        
        



