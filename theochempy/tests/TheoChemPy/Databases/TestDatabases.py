#!/usr/bin/env python
# @author Stefano Borini

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

from Simple import TestDBAccess

suite=unittest.TestSuite()

for test_case_class in [
                TestDBAccess.TestDBAccess,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

