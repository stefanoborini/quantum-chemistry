#!/usr/bin/env python
# @author Stefano Borini - using bazaar now

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

import TestSSHNode

suite=unittest.TestSuite()

for test_case_class in [
                TestSSHNode.TestSSHNode,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

