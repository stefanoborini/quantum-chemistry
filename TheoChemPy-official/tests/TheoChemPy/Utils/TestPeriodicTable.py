# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from TheoChemPy.Utils import PeriodicTable

"""
This is a test suite for the PeriodicTable class.
"""
class TestPeriodicTable(unittest.TestCase):
    def testGetElementBySymbol(self):
        self.assertEqual(PeriodicTable.getElementBySymbol("C"), PeriodicTable.Carbon)
        self.assertEqual(PeriodicTable.getElementBySymbol("N"), PeriodicTable.N)
        self.assertEqual(PeriodicTable.getElementBySymbol("N"), PeriodicTable.Nitrogen)
            
    def testGetElementByAtomicNumber(self):
        self.assertEqual(PeriodicTable.getElementByAtomicNumber(6), PeriodicTable.Carbon)
        self.assertEqual(PeriodicTable.getElementByAtomicNumber(1), PeriodicTable.Hydrogen)

if __name__ == '__main__':
    unittest.main()
    
# vim: et ts=4 sw=4
