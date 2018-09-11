#!/usr/bin/env python
# @author Stefano Borini

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../..")); 
import unittest

from FileParsers.Dalton20 import TestTokenizer
from FileParsers.Dalton20 import TestTokens
from FileParsers.ZMatrix import TestZMatrixParser

suite=unittest.TestSuite()

for test_case_class in [
                TestTokens.TestTokens,
                TestTokenizer.TestTokenizer,
                TestZMatrixParser.TestZMatrixParser,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

