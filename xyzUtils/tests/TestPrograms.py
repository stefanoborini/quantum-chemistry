# @author Stefano Borini
# @license Artistic License 2.0
import os; import sys; script_path=sys.path[0]; sys.path.insert(1,os.path.join(os.path.basename(script_path),"../xyzUtils-1.0.0.package/Libraries/noarch/python/lib/python/"))
import unittest

import hashlib
import string 

def moduleDir():
    return os.path.dirname(__file__)

    
class TestPrograms(unittest.TestCase):
    def testCenter(self):
        filename = os.path.join(moduleDir(),"input","center.xyz")

        program = os.path.join(moduleDir(),"..","Executables", "noarch", "center.py")
        test_output = os.path.join(moduleDir(),"test-testCenter.out")

        try:
            os.unlink(test_output)
        except:
            pass

        os.system("PYTHONPATH=$PYTHONPATH:../xyzUtils-1.0.0.package/Libraries/noarch/python/lib/python/ python "+program+" "+filename+" "+test_output)

        f1 = file(test_output).read()
        f2 = file(os.path.join(moduleDir(),"expected","center.expected")).read()

        md1 = hashlib.md5(f1)
        md2 = hashlib.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())


if __name__ == '__main__':
    unittest.main()
    
