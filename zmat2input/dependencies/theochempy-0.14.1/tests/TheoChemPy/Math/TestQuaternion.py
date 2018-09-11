# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.Math import Quaternion
from theochempy._theochempy import Units 
from theochempy._theochempy import Measure

import math
import warnings

class TestQuaternion(unittest.TestCase):
    def testInit(self): # fold>>

        q = Quaternion(Measure.Measure([1.0,2.0,3.0], Units.angstrom), Measure.Measure(45.0, Units.degrees) )
        
        self.assertAlmostEqual(q._w(), math.cos(math.pi/8.0))
        self.assertAlmostEqual(q._x(), 1.0*math.sin(math.pi/8.0))
        self.assertAlmostEqual(q._y(), 2.0*math.sin(math.pi/8.0))
        self.assertAlmostEqual(q._z(), 3.0*math.sin(math.pi/8.0))

        q = Quaternion(Measure.Measure([1.0,2.0,3.0], Units.angstrom) , Measure.Measure(math.pi/4.0, Units.radians) )
       
        self.assertAlmostEqual(q._w(), math.cos(math.pi/8.0))
        self.assertAlmostEqual(q._x(), 1.0*math.sin(math.pi/8.0))
        self.assertAlmostEqual(q._y(), 2.0*math.sin(math.pi/8.0))
        self.assertAlmostEqual(q._z(), 3.0*math.sin(math.pi/8.0))
        # <<fold
    def testToRotationMatrix(self): # fold>>
        q=Quaternion(Measure.Measure([1.0,0.0,0.0], Units.angstrom) , Measure.Measure(0.0615, Units.radians))
        m = q.toRotationMatrix()
        self.assertAlmostEqual(m[0][0], 1.0)
        self.assertAlmostEqual(m[0][1], 0.0)
        self.assertAlmostEqual(m[0][2], 0.0)
        self.assertAlmostEqual(m[1][0], 0.0)
        self.assertAlmostEqual(m[1][1], math.cos(0.0615))
        self.assertAlmostEqual(m[1][2], -math.sin(0.0615))
        self.assertAlmostEqual(m[2][0], 0.0)
        self.assertAlmostEqual(m[2][1], math.sin(0.0615))
        self.assertAlmostEqual(m[2][2], math.cos(0.0615))

        q=Quaternion(Measure.Measure([1.0,0.0,0.0], Units.angstrom) , Measure.Measure(-0.0615, Units.radians))
        m = q.toRotationMatrix()
        self.assertAlmostEqual(m[0][0], 1.0)
        self.assertAlmostEqual(m[0][1], 0.0)
        self.assertAlmostEqual(m[0][2], 0.0)
        self.assertAlmostEqual(m[1][0], 0.0)
        self.assertAlmostEqual(m[1][1], math.cos(-0.0615))
        self.assertAlmostEqual(m[1][2], -math.sin(-0.0615))
        self.assertAlmostEqual(m[2][0], 0.0)
        self.assertAlmostEqual(m[2][1], math.sin(-0.0615))
        self.assertAlmostEqual(m[2][2], math.cos(-0.0615))
        # <<fold

if __name__ == '__main__':
    unittest.main()
    
