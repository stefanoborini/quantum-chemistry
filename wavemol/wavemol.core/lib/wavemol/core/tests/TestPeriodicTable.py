# @author Stefano Borini

from wavemol.core import chemistry 
from wavemol.core.chemistry import elements
from wavemol.core import units

import unittest
"""
This is a test suite for the PeriodicTable class.
"""
class TestPeriodicTable(unittest.TestCase):
    def testGetElementBySymbol(self):
        self.assertEqual(chemistry.PeriodicTable.element(symbol="C"), elements.C)
        self.assertEqual(chemistry.PeriodicTable.element(symbol="N"), elements.N)
        self.assertEqual(chemistry.PeriodicTable.element(symbol="N"), elements.N)
            
    def testGetElementByAtomicNumber(self):
        self.assertEqual(chemistry.PeriodicTable.element(atomic_number=6), elements.C)
        self.assertEqual(chemistry.PeriodicTable.element(atomic_number=1), elements.H)

    def testElementInterface(self):
        self.assertEqual(elements.He.symbol(), "He")
        self.assertEqual(elements.He.atomicNumber(), 2)
        self.assertAlmostEqual(elements.He.mass().magnitude, 4.0026022)
        self.assertEqual(elements.He.mass().units, units.dalton)
if __name__ == '__main__':
    unittest.main()
    
# vim: et ts=4 sw=4
