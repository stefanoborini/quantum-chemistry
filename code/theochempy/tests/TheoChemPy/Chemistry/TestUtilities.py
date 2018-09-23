# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.Chemistry import Utilities
from theochempy._theochempy.Chemistry import PeriodicTable

"""
This is a test suite for the PeriodicTable class.
"""
class TestPeriodicTable(unittest.TestCase):
    def testHillFormula(self):
        ethanol = [ PeriodicTable.Carbon, 
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Carbon,
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Oxygen,
                    PeriodicTable.Hydrogen
        ]

        self.assertEqual(Utilities.hillFormula(ethanol), "C2H6O")

        ammonia = [ PeriodicTable.Nitrogen, 
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Hydrogen,
                    PeriodicTable.Hydrogen,
        ]

        self.assertEqual(Utilities.hillFormula(ammonia), "H3N") # acccording to Hill
            
if __name__ == '__main__':
    unittest.main()
    
# vim: et ts=4 sw=4
