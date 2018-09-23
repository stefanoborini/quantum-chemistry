# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../../"));
import unittest
import tempfile

from TheoChemPy import Units
from TheoChemPy.Utils import PeriodicTable
from TheoChemPy.InputGenerators import Dalton20

class TestMolFile(unittest.TestCase):
    def testMolFile_1(self):
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, (1.0,0.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, (0.0,1.0,0.0), Units.Angstrom, "hello")
        d.addAtom("C2",PeriodicTable.C, (0.0,2.0,0.0), Units.Angstrom, "hello")

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_1())
    
    def testMolFile_2(self):
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, (1.0,0.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, (0.0,1.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, (0.0,2.0,0.0), Units.Angstrom, "cc-pVDZ")

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_2())

    def testMolFile_3(self):
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, (1.0,0.0,0.0), Units.Bohr, "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, (0.0,1.0,0.0), Units.Bohr, "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, (0.0,2.0,0.0), Units.Bohr, "cc-pVDZ")

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_3())

    def testMolFile_4(self):
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, (1.0,0.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, (0.0,1.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.addAtom("C2",PeriodicTable.C, (0.0,2.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.forceAtomBasis(True)

        out = d.generateOutput()
        self.assertEqual(out, expectedMolFileResult_4())

    def testMolFile_WrongUnits(self):
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, (1.0,0.0,0.0), Units.degrees, "cc-pVDZ")

        self.assertRaises(Exception, d.generateOutput)

    def testMolFile_MixedUnits(self):
        d = Dalton20.MolFile()
        d.addComment("hello","ciao")
        d.addAtom("H1",PeriodicTable.H, (1.0,0.0,0.0), Units.Angstrom, "cc-pVDZ")
        d.addAtom("C1",PeriodicTable.C, (0.0,1.0,0.0), Units.Bohr, "cc-pVDZ")

        self.assertRaises(Exception, d.generateOutput)

def expectedMolFileResult_1():
    return """ATOMBASIS
hello
ciao
Angstrom Atomtypes=2
Charge=6.0 Atoms=2 Basis=hello
C1      0.000000    1.000000    0.000000
C2      0.000000    2.000000    0.000000
Charge=1.0 Atoms=1 Basis=cc-pVDZ
H1      1.000000    0.000000    0.000000
"""

def expectedMolFileResult_2():
    return """BASIS
cc-pVDZ
hello
ciao
Angstrom Atomtypes=2
Charge=6.0 Atoms=2
C1      0.000000    1.000000    0.000000
C2      0.000000    2.000000    0.000000
Charge=1.0 Atoms=1
H1      1.000000    0.000000    0.000000
"""

def expectedMolFileResult_3():
    return """BASIS
cc-pVDZ
hello
ciao
Atomtypes=2
Charge=6.0 Atoms=2
C1      0.000000    1.000000    0.000000
C2      0.000000    2.000000    0.000000
Charge=1.0 Atoms=1
H1      1.000000    0.000000    0.000000
"""

def expectedMolFileResult_4():
    return """ATOMBASIS
hello
ciao
Angstrom Atomtypes=2
Charge=6.0 Atoms=2 Basis=cc-pVDZ
C1      0.000000    1.000000    0.000000
C2      0.000000    2.000000    0.000000
Charge=1.0 Atoms=1 Basis=cc-pVDZ
H1      1.000000    0.000000    0.000000
"""

if __name__ == '__main__':
    unittest.main()
    
# vim: et ts=4 sw=4
