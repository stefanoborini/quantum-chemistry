# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../"));
import unittest

from theochempy._theochempy import Units

class TestUnits(unittest.TestCase):
    def testBytes(self): # fold>>
        self.assertEqual(Units.kibyte.as(Units.kbyte).asNumber(), 1.024)
        self.assertEqual(Units.kbyte.as(Units.kibyte).asNumber(), .9765625)
        # <<fold

if __name__ == '__main__':
    unittest.main()
    

