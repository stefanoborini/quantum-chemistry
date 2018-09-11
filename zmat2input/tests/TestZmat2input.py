# @author Stefano Borini
# @license Artistic License 2.0
import os; import sys; script_path=sys.path[0]; 
import unittest

import md5

def moduleDir():
    return os.path.dirname(__file__)

def run(program, infile, outfile, optstring="", redirect_stdout=False):
    if redirect_stdout:
        execute = "PYTHONPATH=$PYTHONPATH:../dependencies/theochempy-0.15.0 python "+program+" "+optstring+" "+infile+" >"+os.path.join(moduleDir(),outfile)
    else:
        execute = "PYTHONPATH=$PYTHONPATH:../dependencies/theochempy-0.15.0 python "+program+" "+optstring+" "+infile+" "+os.path.join(moduleDir(),outfile)
    return os.system(execute)

    
class TestZMat2input(unittest.TestCase):
    def testProgram(self):
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")

        program = os.path.join(moduleDir(),"..","Executables","noarch","zmat2input.py")
        test_output = os.path.join(moduleDir(),"test-testProgram.out")

        try:
            os.unlink(test_output)
        except:
            pass

        run(program, filename, test_output)

        f1 = file(test_output).read()
        f2 = file(os.path.join(moduleDir(),"expected", "HSO2POEtg3.expected_out")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())

    def notestProgramPreserveLabels(self):
        filename = os.path.join(moduleDir(),"HSO2POEtg3.zmat")

        program = os.path.join(moduleDir(),"..","Executables","noarch","zmat2input.py")
        test_output = os.path.join(moduleDir(),"test-testProgramPreserveLabels.out")
        try:
            os.unlink(test_output)
        except:
            pass

        run(program, filename, test_output, " --preserve-labels ")

        f1 = file(test_output).read()
        f2 = file(os.path.join(moduleDir(),"expected", "HSO2POEtg3.preserve_labels_expected_out")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())

if __name__ == '__main__':
    unittest.main()
    
