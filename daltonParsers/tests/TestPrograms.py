# @author Stefano Borini
# @license Artistic License 2.0
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "..","dependencies","theochempy-0.14.2"));
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

class TestPrograms(unittest.TestCase):
    def testCCBondLengths(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","CCBondLengths.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","CCbondLengths.py")

        run(program,filename,os.path.join(moduleDir(),"testfile_CCBondLengths.out"), redirect_stdout=True)

        f1 = file(os.path.join(moduleDir(),"testfile_CCBondLengths.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/CCbondLengths.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_CCBondLengths.out"))
        # <<fold
    def testCCBondLengthsPrime(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","CCBondLengthsPrime.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","CCbondLengths.py")

        run(program,filename,os.path.join(moduleDir(),"testfile_CCBondLengthsPrime.out"), redirect_stdout=True)

        f1 = file(os.path.join(moduleDir(),"testfile_CCBondLengthsPrime.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/CCbondLengthsPrime.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_CCBondLengthsPrime.out"))
        # <<fold
    def testDalOut2DalIn(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","dalOut2DalIn.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalOut2dalIn.py")

        run(program,filename,os.path.join(moduleDir(),"testfile_dalOut2DalIn.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_dalOut2DalIn.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalOut2dalIn.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalOut2DalIn.out"))
        # <<fold
    def testDalOut2DalInBasis(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","dalOut2DalInBasis.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalOut2dalIn.py")

        run(program, filename, os.path.join(moduleDir(),"testfile_dalOut2DalInBasis.out"), optstring=" --basis hello ")

        f1 = file(os.path.join(moduleDir(),"testfile_dalOut2DalInBasis.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalOut2dalInBasis.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalOut2DalInBasis.out"))
        # <<fold  
    def testDalOut2DalInAlign(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","dalOut2DalInAlign.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalOut2dalIn.py")

        run(program, filename, os.path.join(moduleDir(),"testfile_dalOut2DalInAlign.out"), optstring=" --align ")

        f1 = file(os.path.join(moduleDir(),"testfile_dalOut2DalInAlign.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalOut2DalInAlign.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalOut2DalInAlign.out"))
        # <<fold
    def testDalOut2DalInSymmetry(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","pa04opt.log")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalOut2dalIn.py")

        run(program,filename,os.path.join(moduleDir(),"testfile_dalOut2dalInSymmetry.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_dalOut2dalInSymmetry.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalOut2dalInSymmetry.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalOut2dalInSymmetry.out"))
        # <<fold
    def testDalOut2DalInSymmetryWithAlign(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","dalOut2DalInSymmetryWithAlign.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalOut2dalIn.py")

        run(program,filename,os.path.join(moduleDir(),"testfile_dalOut2DalInSymmetryWithAlign.out"),optstring=" --align ")

        f1 = file(os.path.join(moduleDir(),"testfile_dalOut2DalInSymmetryWithAlign.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalOut2DalInSymmetryWithAlign.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalOut2DalInSymmetryWithAlign.out"))
        # <<fold 
    def testDalOut2DalInSymmetryWithAlignRelabelSymbolLetters(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","dalOut2DalInSymmetryWithAlignRelabelSymbolLetters.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalOut2dalIn.py")

        os.system("python "+program+" --align --relabel-symbol=letters "+filename+" "+os.path.join(moduleDir(),"testfile_dalOut2DalInSymmetryWithAlignRelabelSymbolLetters.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_dalOut2DalInSymmetryWithAlignRelabelSymbolLetters.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalOut2DalInSymmetryWithAlignRelabelSymbolLetters.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalOut2DalInSymmetryWithAlignRelabelSymbolLetters.out"))
        # <<fold
    def testAlphaPol(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","run_run_polyacetylene-2-cn-cn.out")
        program = os.path.join(moduleDir(),"..","Executables","noarch","alphaPol.py")

        os.system("python "+program+" "+filename+" >"+os.path.join(moduleDir(),"testfile_alphaPol.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_alphaPol.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/alphaPol.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_alphaPol.out"))
        # <<fold
    def testDipole(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","run_polyacetylene-2-cn-no2.out")
        program = os.path.join(moduleDir(),"..","Executables","noarch","dipole.py")

        os.system("python "+program+" "+filename+" >"+os.path.join(moduleDir(),"testfile_dipole.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_dipole.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dipole.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dipole.out"))
        # <<fold
    def testBetaPol(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","run_run_polyacetylene-2-cn-cn.out")
        program = os.path.join(moduleDir(),"..","Executables","noarch","betaPol.py")

        os.system("python "+program+" "+filename+" >"+os.path.join(moduleDir(),"testfile_betaPol.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_betaPol.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/betaPol.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_betaPol.out"))
        # <<fold
    def testBetaPol2(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","betaPol2.in")
        program = os.path.join(moduleDir(),"..","Executables","noarch","betaPol.py")

        os.system("python "+program+" "+filename+" >"+os.path.join(moduleDir(),"testfile_betaPol2.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_betaPol2.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/betaPol2.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_betaPol2.out"))
        # <<fold
    def testGammaPol(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","gammaPol.in")
        program = os.path.join(moduleDir(),"..","Executables","noarch","gammaPol.py")

        os.system("python "+program+" "+filename+" >"+os.path.join(moduleDir(),"testfile_gammaPol.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_gammaPol.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/gammaPol.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_gammaPol.out"))
        # <<fold
    def testCheckErrorNoError(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","checkErrorNoError.in")
        program = os.path.join(moduleDir(),"..","Executables","noarch","checkError.py")

        ret = os.system("python "+program+" "+filename)
        exitcode = (ret >> 8) & 0xFF

        self.assertEqual(exitcode, 0)
        # <<fold
    def testCheckErrorWithError(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","checkErrorWithError.in")
        program = os.path.join(moduleDir(),"..","Executables","noarch","checkError.py")

        ret = os.system("python "+program+" "+filename)
        exitcode = (ret >> 8) & 0xFF


        self.assertEqual(exitcode, 1)

        # <<fold
    def testDalton2rawcml(self): # fold>>
        filename = os.path.join(moduleDir(),"inputfiles","dalton2rawcml.in")

        program = os.path.join(moduleDir(),"..","Executables","noarch","dalton2rawcml.py")

        os.system("python "+program+" "+filename+" "+os.path.join(moduleDir(),"testfile_dalton2rawcml.out"))

        f1 = file(os.path.join(moduleDir(),"testfile_dalton2rawcml.out")).read()
        f2 = file(os.path.join(moduleDir(),"expected/dalton2rawcml.expected")).read()

        md1 = md5.md5(f1)
        md2 = md5.md5(f2)

        self.assertEqual(md1.hexdigest(), md2.hexdigest())
        os.unlink(os.path.join(moduleDir(),"testfile_dalton2rawcml.out"))
        # <<fold
if __name__ == '__main__':
    unittest.main()
    
