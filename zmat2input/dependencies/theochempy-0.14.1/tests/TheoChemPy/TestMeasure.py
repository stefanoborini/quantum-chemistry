# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

import math

from theochempy._theochempy import Measure
from theochempy._theochempy import Units

class TestMeasure(unittest.TestCase):
    def testMeasure(self): # fold>>
        m = Measure.Measure(10, Units.degrees)
        self.assertEqual(m.value(), 10)
        self.assertEqual(m.unit(), Units.degrees)

        m = Measure.Measure((10,11), Units.degrees)
        self.assertEqual(m.value(), (10,11))
        self.assertEqual(m.unit(), Units.degrees)
        # <<fold
    def testAsUnit(self):
        m = Measure.Measure(10, Units.degrees)
        in_rad = m.asUnit(Units.radians)
        self.assertAlmostEqual(in_rad.value(), math.pi*10.0/180.0)
        self.assertEqual(in_rad.unit(), Units.radians)

    def testAsUnitTuple(self):
        m = Measure.Measure((10,11), Units.degrees)
        in_rad = m.asUnit(Units.radians)
        self.assertEqual(in_rad.value()[0], math.pi*10.0/180.0)
        self.assertEqual(in_rad.value()[1], math.pi*11.0/180.0)
        self.assertEqual(in_rad.unit(), Units.radians)

    def testInvalidConversion(self):
        m = Measure.Measure(10, Units.degrees)
        self.assertRaises( Exception,  m.asUnit, Units.debye)

    def testNegative(self):
        m = -Measure.Measure(10, Units.degrees)
        
        self.assertEqual(m.value(), -10)
        self.assertEqual(m.unit(), Units.degrees)

        m = -Measure.Measure((10,11), Units.degrees)
        in_rad = m.asUnit(Units.radians)
        self.assertEqual(in_rad.value()[0], -math.pi*10.0/180.0)
        self.assertEqual(in_rad.value()[1], -math.pi*11.0/180.0)
        self.assertEqual(in_rad.unit(), Units.radians)

    def testSum(self):
        m1 = Measure.Measure(10, Units.hartree)
        m2 = Measure.Measure(5, Units.eV) 

        m_sum = m1 + m2
        self.assertEqual(m_sum.unit(), Units.hartree)
        self.assertAlmostEqual(m_sum.value(), 10.0+5.0/27.21138386,5)

        m3 = Measure.Measure((10,11), Units.eV)
        m_sum = m1+m3
       
        self.assertEqual(m_sum.unit(), Units.hartree)
        self.assertEqual(len(m_sum.value()), 2)
        self.assertAlmostEqual(m_sum.value()[0], 10.0+10.0/27.21138386,5)
        self.assertAlmostEqual(m_sum.value()[1], 10.0+11.0/27.21138386,5)

        m_sum = m3+m1
        self.assertEqual(m_sum.unit(), Units.eV)
        self.assertEqual(len(m_sum.value()), 2)
        self.assertAlmostEqual(m_sum.value()[0], 10.0*27.21138386+10.0,2) # FIXME this value is too wrong. The tolerance is on the second
                                                                          # digit. Something serious must be done to the units
        self.assertAlmostEqual(m_sum.value()[1], 10.0*27.21138386+11.0,2) 

        m4 = Measure.Measure((12,15), Units.hartree)
        m_sum = m4+m3

        self.assertEqual(m_sum.unit(), Units.hartree)
        self.assertEqual(len(m_sum.value()), 2)
        self.assertAlmostEqual(m_sum.value()[0], 12.0+10.0/27.21138386,5)
        self.assertAlmostEqual(m_sum.value()[1], 15.0+11.0/27.21138386,5)
       
        m_wrong = Measure.Measure(10, Units.bohr)
        self.assertRaises(Exception, m1.__add__, m_wrong)
        self.assertRaises(Exception, m_wrong.__add__, m1)
    def testDiff(self):
        m1 = Measure.Measure(10, Units.hartree)
        m2 = Measure.Measure(5, Units.eV) 

        m_diff = m1 - m2
        self.assertEqual(m_diff.unit(), Units.hartree)
        self.assertAlmostEqual(m_diff.value(), 10.0-5.0/27.21138386,5)

        m3 = Measure.Measure((10,11), Units.eV)
        m_diff = m1-m3
       
        self.assertEqual(m_diff.unit(), Units.hartree)
        self.assertEqual(len(m_diff.value()), 2)
        self.assertAlmostEqual(m_diff.value()[0], 10.0-10.0/27.21138386,5)
        self.assertAlmostEqual(m_diff.value()[1], 10.0-11.0/27.21138386,5)

        m_diff = m3-m1
        self.assertEqual(m_diff.unit(), Units.eV)
        self.assertEqual(len(m_diff.value()), 2)
        self.assertAlmostEqual(m_diff.value()[0], 10.0-10.0*27.21138386,2) # FIXME this value is too wrong. The tolerance is on the second
                                                                           # digit. Something serious must be done to the units
        self.assertAlmostEqual(m_diff.value()[1], 11-10.0*27.21138386,2) 

        m4 = Measure.Measure((12,15), Units.hartree)
        m_diff = m4-m3
        self.assertEqual(m_diff.unit(), Units.hartree)
        self.assertEqual(len(m_diff.value()), 2)
        self.assertAlmostEqual(m_diff.value()[0], 12.0-10.0/27.21138386,5)
        self.assertAlmostEqual(m_diff.value()[1], 15.0-11.0/27.21138386,5)

        m_wrong = Measure.Measure(10, Units.bohr)
        self.assertRaises(Exception, m1.__sub__, m_wrong)
        self.assertRaises(Exception, m_wrong.__sub__, m1)
        
if __name__ == '__main__':
    unittest.main()
    

