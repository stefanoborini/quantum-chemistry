# @author Stefano Borini

from wavemol.core import chemistry 
from wavemol.core.chemistry import elements

import unittest
"""
This is a test suite for the PeriodicTable class.
"""
class TestChemistry(unittest.TestCase):
    def testHillFormula(self):
        ethanol = [ elements.C, 
                    elements.H,
                    elements.H,
                    elements.H,
                    elements.C,
                    elements.H,
                    elements.H,
                    elements.O,
                    elements.H
        ]

        self.assertEqual(chemistry.hillFormula(ethanol), "C2H6O")

        ammonia = [ elements.N, 
                    elements.H,
                    elements.H,
                    elements.H,
        ]

        self.assertEqual(chemistry.hillFormula(ammonia), "H3N") # acccording to Hill

        ammonia= [ "H", "N", "H", "H" ]
        self.assertEqual(chemistry.hillFormula(ammonia), "H3N") 

        ammonia= [ 1, 1, 1, 7]
        self.assertEqual(chemistry.hillFormula(ammonia), "H3N") 


if __name__ == '__main__':
    unittest.main()
 


# vim: et ts=4 sw=4
