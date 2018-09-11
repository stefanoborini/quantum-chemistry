# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.Math import Vector3
from theochempy._theochempy import Units
from theochempy._theochempy import Measure
import math

class TestVector3(unittest.TestCase):
    def testInit(self): # fold>>
        v = Vector3(1.0,2.0,3.0)
       
        self.assertAlmostEqual(v.x(), 1.0)
        self.assertAlmostEqual(v.y(), 2.0)
        self.assertAlmostEqual(v.z(), 3.0)

        # <<fold

    def testRotation(self): # fold>>
        v = Vector3(2.0,0.0,0.0)
       
        v.rotate(Measure.Measure(45,Units.degrees), Measure.Measure( (1.0, 0.0, 0.0), Units.bohr))

        self.assertAlmostEqual(v.x(), 2.0)
        self.assertAlmostEqual(v.y(), 0.0)
        self.assertAlmostEqual(v.z(), 0.0)

        v = Vector3(0.0,2.0,0.0)
       
        v.rotate(Measure.Measure(45, Units.degrees), Measure.Measure( (1.0, 0.0, 0.0), Units.bohr))

        self.assertAlmostEqual(v.x(), 0.0)
        self.assertAlmostEqual(v.y(), 2.0/math.sqrt(2.0))
        self.assertAlmostEqual(v.z(), 2.0/math.sqrt(2.0))

        v = Vector3(0.0,2.0,0.0)
       
        v.rotate(Measure.Measure(-45,Units.degrees), Measure.Measure( (1.0, 0.0, 0.0), Units.bohr))

        self.assertAlmostEqual(v.x(), 0.0)
        self.assertAlmostEqual(v.y(), 2.0/math.sqrt(2.0))
        self.assertAlmostEqual(v.z(), -2.0/math.sqrt(2.0))
        
        # <<fold
    def testNorm(self): # fold>>
        v = Vector3(1.0,2.0,-3.0)
       
        self.assertAlmostEqual(v.norm(), math.sqrt(14.0))
        # <<fold

if __name__ == '__main__':
    unittest.main()
    
