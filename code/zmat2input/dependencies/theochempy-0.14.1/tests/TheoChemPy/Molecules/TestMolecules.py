#!/usr/bin/env python
# @author Stefano Borini - using bazaar now

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

import TestXYZMolecule

suite=unittest.TestSuite()

for test_case_class in [
                TestXYZMolecule.TestXYZMolecule,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

