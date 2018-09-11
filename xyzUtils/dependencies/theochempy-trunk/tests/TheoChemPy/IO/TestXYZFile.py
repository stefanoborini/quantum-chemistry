# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.IO import XYZFile
from theochempy._theochempy.Chemistry import PeriodicTable
from theochempy._theochempy import Measure
from theochempy._theochempy import Units

import hashlib 
def moduleDir():
    return os.path.dirname(__file__)

    
class TestXYZFile(unittest.TestCase):
    def testInit(self): # fold>>
        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_simple.xyz"))
        self.assertEqual(xyz.__class__, XYZFile.XYZFile)
        # <<fold
    def testInit2(self): # fold>>
        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_multiple.xyz"))
        self.assertEqual(xyz.__class__, XYZFile.XYZFile)
        # <<fold
    def testNumOfMolecules(self): # fold>>
        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_simple.xyz"))
        self.assertEqual(xyz.numOfMolecules(), 1)

        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_multiple.xyz"))
        self.assertEqual(xyz.numOfMolecules(), 2)
        # <<fold

    def testCommentReturnsNone(self):
        xyz = XYZFile.XYZFile()
        self.assertEqual(xyz.comment(), None)
        self.assertEqual(xyz.comment(1), None)

    def testGetData(self):
        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_simple.xyz"))
        self.assertEqual(xyz.numOfAtoms(),12)
        self.assertEqual(xyz.comment(), "benzene example")
        self.assertEqual(xyz.atom(3)[0], PeriodicTable.Hydrogen)
        self.assertEqual(xyz.atom(3)[1].__class__, Measure.Measure)
        self.assertEqual(xyz.atom(3)[1].value(),  (-2.15666, 1.24515, 0.00000 ))
        self.assertEqual(xyz.atom(3)[1].unit(), Units.angstrom)

    def testGetData2(self):
        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_multiple.xyz"))
        self.assertEqual(xyz.numOfAtoms(0),2)
        self.assertEqual(xyz.comment(0), "benzene single")
        self.assertEqual(xyz.atom(0,1)[0], PeriodicTable.Hydrogen)
        self.assertEqual(xyz.atom(0,1)[1].__class__, Measure.Measure)
        self.assertEqual(xyz.atom(0,1)[1].value(),  (0.0000, 2.49029, 0.00000 ))
        self.assertEqual(xyz.atom(0,1)[1].unit(), Units.angstrom)

        xyz = XYZFile.XYZFile(os.path.join(moduleDir(),"testfile_multiple.xyz"))
        self.assertEqual(xyz.numOfAtoms(),12)
        self.assertEqual(xyz.comment(), "benzene example")
        self.assertEqual(xyz.atom(3)[0], PeriodicTable.Hydrogen)
        self.assertEqual(xyz.atom(3)[1].__class__, Measure.Measure)
        self.assertEqual(xyz.atom(3)[1].value(),  (-2.15666, 1.24515, 0.00000 ))
        self.assertEqual(xyz.atom(3)[1].unit(), Units.angstrom)

    def testCreateMolecule(self):
        xyz = XYZFile.XYZFile()
        self.assertEqual(xyz.createMolecule(), 0)
        self.assertEqual(xyz.createMolecule(), 1)
        self.assertEqual(xyz.createMolecule(1), 1)

        self.assertEqual(xyz.numOfMolecules(), 3)

    def testSetComment(self):
        xyz = XYZFile.XYZFile()
        xyz.createMolecule()
        xyz.setComment("hello")
        self.assertEqual(xyz.comment(), "hello")

        xyz.createMolecule()
        xyz.setComment("hello 2")
        self.assertEqual(xyz.comment(), "hello 2")

        xyz.setComment(0,"hello 1")
        self.assertEqual(xyz.comment(0), "hello 1")
        self.assertEqual(xyz.comment(1), "hello 2")
        self.assertEqual(xyz.comment(), "hello 2")

        self.assertRaises(IndexError, xyz.setComment, 2,"hello" )
    def testAddAtom(self):
        xyz = XYZFile.XYZFile()
        xyz.createMolecule()
        xyz.setComment("hello")
        xyz.addAtom((PeriodicTable.Hydrogen, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))
        xyz.addAtom((PeriodicTable.Carbon, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))
        
        self.assertEqual(xyz.atom(0)[0], PeriodicTable.Hydrogen)
        self.assertEqual(xyz.atom(1)[0], PeriodicTable.Carbon)

    def testAddAtom2(self):
        xyz = XYZFile.XYZFile()
        xyz.createMolecule()
        xyz.setComment("hello")
        xyz.addAtom((PeriodicTable.Hydrogen, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))
        xyz.addAtom((PeriodicTable.Carbon, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))

        xyz.createMolecule()
        xyz.setComment("hello")
        xyz.addAtom((PeriodicTable.Oxygen, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))
        xyz.addAtom((PeriodicTable.Fluorine, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))
        
        self.assertEqual(xyz.atom(0)[0], PeriodicTable.Oxygen)
        self.assertEqual(xyz.atom(1)[0], PeriodicTable.Fluorine)

        self.assertEqual(xyz.atom(1,0)[0], PeriodicTable.Oxygen)
        self.assertEqual(xyz.atom(1,1)[0], PeriodicTable.Fluorine)

        self.assertEqual(xyz.atom(0,0)[0], PeriodicTable.Hydrogen)
        self.assertEqual(xyz.atom(0,1)[0], PeriodicTable.Carbon)

    def testSaveTo(self):
        xyz = XYZFile.XYZFile()
        xyz.createMolecule()
        xyz.setComment("hello 1")
        xyz.addAtom((PeriodicTable.Hydrogen, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))
        xyz.addAtom((PeriodicTable.Carbon, Measure.Measure( (1.0, 2.0, 3.0), Units.angstrom)))

        xyz.createMolecule()
        xyz.setComment("hello 2")
        xyz.addAtom((PeriodicTable.Oxygen, Measure.Measure( (4.0, 6.0, 8.0), Units.angstrom)))
        xyz.addAtom((PeriodicTable.Fluorine, Measure.Measure( (5.0, 7.0, 9.0), Units.angstrom)))
        
        xyz.saveTo(os.path.join(moduleDir(),"testfile_saveTo.xyz"))
        f1 = file(os.path.join(moduleDir(),"testfile_saveTo.xyz")).read()
        f2 = file(os.path.join(moduleDir(),"saveTo.expected")).read()
    
        md1 = hashlib.md5(f1)
        md2 = hashlib.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_saveTo.xyz"))
        # <<fold

if __name__ == '__main__':
    unittest.main()
