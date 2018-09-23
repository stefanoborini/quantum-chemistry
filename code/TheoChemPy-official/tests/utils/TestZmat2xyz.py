# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; 
sys.path.append(os.path.join(script_path, "../../"));
sys.path.append(os.path.join(script_path, "../../utils"));
import unittest

from TheoChemPy.IO import FileReader
from TheoChemPy import Math
from TheoChemPy.Utils import zmatmodule
import hashlib
import string 
def moduleDir():
    return os.path.dirname(__file__)

    
class TestZMat2xyz(unittest.TestCase):
    def testProgram(self):
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")

        program = os.path.join("..","..","utils","zmat2input")

        os.system("PYTHONPATH=\""+string.join(sys.path,":")+":../..\" "+program+" "+filename+" "+os.path.join(moduleDir(),"test.out"))

        f1 = file(os.path.join(moduleDir(),"test.out")).read()
        f2 = file(os.path.join(moduleDir(),"HSO2POEtg3.expected_out")).read()

        md1 = hashlib.md5(f1)
        md2 = hashlib.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())

if __name__ == '__main__':
    unittest.main()
    
