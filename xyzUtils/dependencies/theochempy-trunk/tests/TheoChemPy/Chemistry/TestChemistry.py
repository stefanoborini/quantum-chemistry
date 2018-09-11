#!/usr/bin/env python
# @author Stefano Borini

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

import TestPeriodicTable

suite=unittest.TestSuite()

for test_case_class in [
                TestPeriodicTable.TestPeriodicTable,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

