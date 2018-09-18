import subprocess
from theochempy._theochempy import Units

# private symbols to describe the dictionary keys. you should never use them. Used in the test
_SETTING_DALTON_SCRIPT_PATH="dalton_script_path"
_SETTING_BASIS_SET_PATH="basis_set_path" 
_SETTING_DELETE_SCRATCH_BEFORE="delete_scratch_before"
_SETTING_DELETE_SCRATCH_AFTER="delete_scratch_after"
_SETTING_OUTPUT_EXTENSION="output_extension" 
_SETTING_REDIRECT_OUTPUT="redirect_output"
_SETTING_USE_DALMOL_TGZ="use_dalmol_tgz"
_SETTING_SCRATCH_MEM="scratch_mem"
_SETTING_MPI_NUM_NODES ="mpi_num_nodes" 
_SETTING_LAM_FILE="lam_file"
_SETTING_TEMP_DIR="temp_dir"
_SETTING_WORK_DIR="work_dir"


class Dalton20:
    def __init__(self, settings):
        self._settings = settings 
    def run(self, molfile_path, dalfile_path):

        args = _createArgumentList(self._settings)
        args.append(molfile_path)
        args.append(dalfile_path)

        return subprocess.Popen(args)

def _createArgumentList(settings): # fold>>
    args = []
    args.append(settings[_SETTING_DALTON_SCRIPT_PATH])
    
    if settings[_SETTING_BASIS_SET_PATH] is not None:
        args.append("-b")
        args.append(settings[_SETTING_BASIS_SET_PATH])

    if settings[_SETTING_DELETE_SCRATCH_BEFORE] is not None and settings[_SETTING_DELETE_SCRATCH_BEFORE] == True:
        args.append("-d")
   
    if settings[_SETTING_DELETE_SCRATCH_AFTER] is not None and settings[_SETTING_DELETE_SCRATCH_AFTER] == False:
        args.append("-D")

    if settings[_SETTING_OUTPUT_EXTENSION] is not None:
        args.append("-ext")
        args.append(settings[_SETTING_OUTPUT_EXTENSION])

    if settings[_SETTING_REDIRECT_OUTPUT] is not None:
        args.append("-o")
        args.append(settings[_SETTING_REDIRECT_OUTPUT])

    if settings[_SETTING_USE_DALMOL_TGZ] is not None:
        args.append("-f")
        args.append(settings[_SETTING_USE_DALMOL_TGZ])

    if settings[_SETTING_SCRATCH_MEM] is not None:
        args.append("-M")
        value = settings[_SETTING_SCRATCH_MEM].value()
        unit = settings[_SETTING_SCRATCH_MEM].unit()
        mebibytes = str(int((value*unit).as(Units.Mibyte).asNumber()))
        args.append(mebibytes)

    if settings[_SETTING_MPI_NUM_NODES] is not None:
        args.append("-N")
        args.append(str(settings[_SETTING_MPI_NUM_NODES]))

    if settings[_SETTING_LAM_FILE] is not None:
        args.append("-lam")
        args.append(settings[_SETTING_LAM_FILE])

    if settings[_SETTING_TEMP_DIR] is not None:
        args.append("-t")
        args.append(settings[_SETTING_TEMP_DIR])

    if settings[_SETTING_WORK_DIR] is not None:
        args.append("-w")
        args.append(settings[_SETTING_WORK_DIR])
    return args
# <<fold

# scratch mem disabled as we need to accept a unit qualified value

def daltonSettings(dalton_script_path, 
                    basis_set_path=None, 
                    delete_scratch_before=None, 
                    delete_scratch_after=None, 
                    output_extension=None,
                    redirect_output=None,
                    use_dalmol_tgz=None,
                    scratch_mem=None,
                    mpi_num_nodes=None,
                    lam_file=None,
                    temp_dir=None,
                    work_dir=None,
                    ):

    return { _SETTING_DALTON_SCRIPT_PATH : dalton_script_path, 
             _SETTING_BASIS_SET_PATH : basis_set_path,
             _SETTING_DELETE_SCRATCH_BEFORE : delete_scratch_before,
             _SETTING_DELETE_SCRATCH_AFTER : delete_scratch_after,
             _SETTING_OUTPUT_EXTENSION : output_extension,
             _SETTING_REDIRECT_OUTPUT : redirect_output,
             _SETTING_USE_DALMOL_TGZ : use_dalmol_tgz,
             _SETTING_SCRATCH_MEM : scratch_mem,
             _SETTING_MPI_NUM_NODES : mpi_num_nodes,
             _SETTING_LAM_FILE : lam_file,
             _SETTING_TEMP_DIR : temp_dir,
             _SETTING_WORK_DIR : work_dir,
             }


class DaltonEngine:
    def firstHyperpolarizabilityEvaluator(): 
        return FirstHyperPolarizabilityEvaluator()



class FirstHyperPolarizabilityEvaluator:
    def __init__(self, **args): pass
    def evaluate(self, molfile=None): pass
        




def _createDalFileFirstHyperpolarizability(frequencies):
    string = """**DALTON
.RUN RESPONS
.DIRECT
**INTEGRALS
.DIPLEN
.NOSUP
*END OF HERMIT
**WAVE FUNCTIONS
.DFT
CAMB3LYP
*SCF INP
.THRESH
1.0D-8
.MAX DIIS ITERATIONS
100
*ORBITAL INP
.AO DELETE
1.0D-3
**RESPONS
*CUBIC
.DIPLEN
.THG
.FREQUE
"""
    string += str(len(frequencies))+'\n'
    for f in frequencies:
        string += str(f.asUnit(Units.hartree).value())+" "
    string += "\n"
    string += "**END OF DALTON INPUT"

