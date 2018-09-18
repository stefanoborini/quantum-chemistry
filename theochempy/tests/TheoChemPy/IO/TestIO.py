#!/usr/bin/env python
# @author Stefano Borini - using bazaar now

import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../")); 
import unittest

from IO import TestFileReader
from IO import TestDirWalker
from IO import TestCSVFile
from IO import TestXYZFile

suite=unittest.TestSuite()

for test_case_class in [
                TestFileReader.TestFileReader,
                TestDirWalker.TestDirWalker,
                TestCSVFile.TestCSVFile,
                TestXYZFile.TestXYZFile,
                ]:
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_case_class))




    

