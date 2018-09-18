# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.Engines import Dalton20
from theochempy._theochempy import Units 
from theochempy._theochempy import Measure
import string

class TestDalton20(unittest.TestCase):
    def testDaltonSettings(self): # fold>>
        settings = Dalton20.daltonSettings(dalton_script_path = "/foo/bar")
        self.assertEqual(settings[Dalton20._SETTING_DALTON_SCRIPT_PATH], "/foo/bar")
        self.assertEqual(settings[Dalton20._SETTING_BASIS_SET_PATH], None)
        self.assertEqual(settings[Dalton20._SETTING_DELETE_SCRATCH_BEFORE], None)
        self.assertEqual(settings[Dalton20._SETTING_DELETE_SCRATCH_AFTER], None)
        self.assertEqual(settings[Dalton20._SETTING_OUTPUT_EXTENSION], None)
        self.assertEqual(settings[Dalton20._SETTING_REDIRECT_OUTPUT], None)
        self.assertEqual(settings[Dalton20._SETTING_USE_DALMOL_TGZ], None)
        self.assertEqual(settings[Dalton20._SETTING_SCRATCH_MEM], None)
        self.assertEqual(settings[Dalton20._SETTING_MPI_NUM_NODES], None)
        self.assertEqual(settings[Dalton20._SETTING_LAM_FILE], None)
        self.assertEqual(settings[Dalton20._SETTING_TEMP_DIR], None)
        self.assertEqual(settings[Dalton20._SETTING_WORK_DIR], None)

        settings = Dalton20.daltonSettings(dalton_script_path = "/foo/bar", 
                                           basis_set_path = "baz/fru",
                                           delete_scratch_before = True,
                                           delete_scratch_after = False,
                                           output_extension = "foo",
                                           redirect_output = "hello",
                                           use_dalmol_tgz = "cucu",
                                           scratch_mem = Measure.Measure(10.0, Units.Mbyte),
                                           mpi_num_nodes = 16,
                                           lam_file = "foox",
                                           temp_dir = "/foo/xu",
                                           work_dir = "/foo/mu")
        self.assertEqual(settings[Dalton20._SETTING_DALTON_SCRIPT_PATH], "/foo/bar")
        self.assertEqual(settings[Dalton20._SETTING_BASIS_SET_PATH], "baz/fru")
        self.assertEqual(settings[Dalton20._SETTING_DELETE_SCRATCH_BEFORE], True)
        self.assertEqual(settings[Dalton20._SETTING_DELETE_SCRATCH_AFTER], False)
        self.assertEqual(settings[Dalton20._SETTING_OUTPUT_EXTENSION], "foo")
        self.assertEqual(settings[Dalton20._SETTING_REDIRECT_OUTPUT], "hello")
        self.assertEqual(settings[Dalton20._SETTING_USE_DALMOL_TGZ], "cucu")
        self.assertEqual(settings[Dalton20._SETTING_SCRATCH_MEM].value(), 10.0)
        self.assertEqual(settings[Dalton20._SETTING_SCRATCH_MEM].unit(), Units.Mbyte)
        self.assertEqual(settings[Dalton20._SETTING_MPI_NUM_NODES], 16)
        self.assertEqual(settings[Dalton20._SETTING_LAM_FILE], "foox")
        self.assertEqual(settings[Dalton20._SETTING_TEMP_DIR], "/foo/xu")
        self.assertEqual(settings[Dalton20._SETTING_WORK_DIR], "/foo/mu")


        # <<fold
     
    def testArgumentList(self): # fold>>
        settings = Dalton20.daltonSettings(dalton_script_path = "/foo/bar")

        self.assertEqual(string.join(Dalton20._createArgumentList(settings)), "/foo/bar")

        settings = Dalton20.daltonSettings(dalton_script_path = "/foo/bar", 
                                           basis_set_path = "baz/fru",
                                           delete_scratch_before = True,
                                           delete_scratch_after = False,
                                           output_extension = "foo",
                                           redirect_output = "hello",
                                           scratch_mem = Measure.Measure(1, Units.Gbyte),
                                           use_dalmol_tgz = "cucu",
                                           mpi_num_nodes = 16,
                                           lam_file = "foox",
                                           temp_dir = "/foo/xu",
                                           work_dir = "/foo/mu")

        self.assertEqual(string.join(Dalton20._createArgumentList(settings)), "/foo/bar -b baz/fru -d -D -ext foo -o hello -f cucu -M 953 -N 16 -lam foox -t /foo/xu -w /foo/mu")


        # <<fold

if __name__ == '__main__':
    unittest.main()
    

