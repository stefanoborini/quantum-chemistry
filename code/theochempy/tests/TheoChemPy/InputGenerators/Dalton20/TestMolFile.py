# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest

from theochempy._theochempy import Units
from theochempy._theochempy import Measure
from theochempy._theochempy.Chemistry import PeriodicTable
from theochempy._theochempy.InputGenerators import Dalton20

class TestMolFile(unittest.TestCase):
    def testMolFile_1(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, Measure.Measure((0.0,1.0,0.0), Units.angstrom), "hello")
        d.addAtom("C2",PeriodicTable.C, Measure.Measure((0.0,2.0,0.0), Units.angstrom), "hello")

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_1())
        # <<fold 
    def testMolFile_2(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, Measure.Measure((0.0,1.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, Measure.Measure((0.0,2.0,0.0), Units.angstrom), "cc-pVDZ")

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_2())
        # <<fold
    def testMolFile_3(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.bohr), "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, Measure.Measure((0.0,1.0,0.0), Units.bohr), "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, Measure.Measure((0.0,2.0,0.0), Units.bohr), "cc-pVDZ")

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_3())
        # <<fold
    def testMolFile_4(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, Measure.Measure((0.0,1.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, Measure.Measure((0.0,2.0,0.0), Units.angstrom), "cc-pVDZ")
        d.forceAtomBasis(True)

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_4())
        # <<fold
    def testMolFile_checkOrderOfGroups(self): # fold>>
        """check if the increasing order is respected"""
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("O1",PeriodicTable.O, Measure.Measure((0.0,3.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, Measure.Measure((0.0,1.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, Measure.Measure((0.0,2.0,0.0), Units.angstrom), "cc-pVDZ")
        d.forceAtomBasis(True)

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_orderOfGroups())
        # <<fold
    def testMolFile_WrongUnits(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.degrees), "cc-pVDZ")

        self.assertRaises(Exception, d.generateOutput)
        # <<fold
    def testMolFile_MixedUnits(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, Measure.Measure((1.0,0.0,0.0), Units.angstrom), "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, Measure.Measure((0.0,1.0,0.0), Units.bohr), "cc-pVDZ")

        self.assertRaises(Exception, d.generateOutput)
        # <<fold
    def testMolFile_NoAtoms(self): # fold>>
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")

        self.assertRaises(Exception, d.generateOutput)
        # <<fold

def expectedMolFileResult_1(): # fold>>
    return """ATOMBASIS
hello
ciao
Angstrom Atomtypes=2
Charge=1.0 Atoms=1 Basis=cc-pVDZ
H1      1.000000000000    0.000000000000    0.000000000000
Charge=6.0 Atoms=2 Basis=hello
C1      0.000000000000    1.000000000000    0.000000000000
C2      0.000000000000    2.000000000000    0.000000000000
"""
# <<fold
def expectedMolFileResult_2(): # fold>>
    return """BASIS
cc-pVDZ
hello
ciao
Angstrom Atomtypes=2
Charge=1.0 Atoms=1
H1      1.000000000000    0.000000000000    0.000000000000
Charge=6.0 Atoms=2
C1      0.000000000000    1.000000000000    0.000000000000
C2      0.000000000000    2.000000000000    0.000000000000
"""
# <<fold
def expectedMolFileResult_3(): # fold>>
    return """BASIS
cc-pVDZ
hello
ciao
Atomtypes=2
Charge=1.0 Atoms=1
H1      1.000000000000    0.000000000000    0.000000000000
Charge=6.0 Atoms=2
C1      0.000000000000    1.000000000000    0.000000000000
C2      0.000000000000    2.000000000000    0.000000000000
"""
# <<fold
def expectedMolFileResult_4(): # fold>> 
    return """ATOMBASIS
hello
ciao
Angstrom Atomtypes=2
Charge=1.0 Atoms=1 Basis=cc-pVDZ
H1      1.000000000000    0.000000000000    0.000000000000
Charge=6.0 Atoms=2 Basis=cc-pVDZ
C1      0.000000000000    1.000000000000    0.000000000000
C2      0.000000000000    2.000000000000    0.000000000000
"""
# <<fold
def expectedMolFileResult_orderOfGroups(): # fold>>
    return """ATOMBASIS
hello
ciao
Angstrom Atomtypes=3
Charge=1.0 Atoms=1 Basis=cc-pVDZ
H1      1.000000000000    0.000000000000    0.000000000000
Charge=6.0 Atoms=2 Basis=cc-pVDZ
C1      0.000000000000    1.000000000000    0.000000000000
C2      0.000000000000    2.000000000000    0.000000000000
Charge=8.0 Atoms=1 Basis=cc-pVDZ
O1      0.000000000000    3.000000000000    0.000000000000
"""
# <<fold

if __name__ == '__main__':
    unittest.main()
    
# vim: et ts=4 sw=4
