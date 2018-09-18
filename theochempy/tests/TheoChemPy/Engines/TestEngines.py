#!/usr/bin/env python
# @author Stefano Borini

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

import TestDalton20

suite=unittest.TestSuite()

for test_case_class in [
                TestDalton20.TestDalton20,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

