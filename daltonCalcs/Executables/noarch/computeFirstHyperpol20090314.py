#/usr/bin/env python
# @author Stefano Borini
# @description runs computation for first hyperpol
# @license Artistic License 2.0

import getopt
import os
import sys

def _usage():
    print "Usage : "+os.path.basename(sys.argv[0])+" [--x-only] [--frequencies=0.0,0.01,...]"
    print ""
    print "Computes the first hyperpolarizabilities for a given dalton file"
    print ""
    print "Options:"
    print ""
    print "--x-only               : Computes only along the (X;X,X) component"
    print "--frequencies=0.0,0.01 : Calculates for the given frequencies, in hartree, comma separated."
    print "                         If not specified, only the static (freq=0.0) is computed"
    print ""

opts, args=getopt.getopt(sys.argv[1:], "f:xh", ["frequencies=", "x-only", "help"])

frequencies=None
x_only = False

for opt in opts:
    if opt[0] == "-f" or opt[0] == "--frequencies":
        frequencies = opt[1].split(",")
    if opt[0] == "-x" or opt[0] == "--x-only":
        x_only = True
    if opt[0] == "-h" or opt[0] == "--help":
        _usage()
        sys.exit(1)

if len(args) < 1:
    _usage()
    sys.exit(1)

dalton_mol_filename = args[0]
if frequencies is None:
    frequencies = ["0.00"]

f = file(os.path.join(os.getcwd(),"run.dal"),"w")
f.write("""# this file generated automatically by computeFirstHyperpol20090314.py
**DALTON
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
1.0D-7
.MAX DIIS ITERATIONS
 100
*ORBITAL INP
.AO DELETE
1.0D-2
**RESPONS
*QUADRA
""")
if x_only:
    f.write(".DIPLNX\n")
else:
    f.write(".DIPLEN\n")
f.write(".FREQUE\n")
f.write(" "+str(len(frequencies))+"\n")
for freq in frequencies:
    f.write(freq+" ")
f.write("\n")
f.write("**END OF DALTON INPUT\n")
f.close()

sys.exit(os.system("cnrun dalton-2 run "+os.path.splitext(dalton_mol_filename)[0]))

