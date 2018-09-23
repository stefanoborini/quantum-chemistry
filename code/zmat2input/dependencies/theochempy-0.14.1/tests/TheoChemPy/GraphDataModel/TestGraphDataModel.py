#!/usr/bin/env python
# @author Stefano Borini - using bazaar now

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

import TestGraph
import TestInfosets

suite=unittest.TestSuite()

for test_case_class in [
                TestGraph.TestGraph,
                TestInfosets.TestInfosets,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite)

    

