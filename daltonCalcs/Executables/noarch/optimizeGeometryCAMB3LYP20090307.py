#/usr/bin/env python
# @author Stefano Borini
# @description this script performs geometry optimization CAM-B3LYP
# @license Artistic License 2.0

import getopt
import os
import sys

def _usage():
    print "Usage : "+os.path.basename(sys.argv[0])+" dalton_mol_file "
    print ""
    print "Performs a CAM-B3LYP geometry optimization for a given dalton file"
    print ""

opts, args=getopt.getopt(sys.argv[1:], "h", ["help"])

frequencies=None
x_only = False

for opt in opts:
    if opt[0] == "-h" or opt[0] == "--help":
        _usage()
        sys.exit(1)

if len(args) < 1:
    _usage()
    sys.exit(1)

dalton_mol_filename = args[0]

f = file(os.path.join(os.getcwd(),"run.dal"),"w")
f.write("""**DALTON
.DIRECT
.RUN WAVE FUNCTION
.OPTIMIZE
**INTEGRALS
.NOSUP
*END OF HERMIT
**WAVE FUNCTIONS
.DFT
CAMB3LYP
*END OF
""")
f.close()

sys.exit(os.system("cnrun dalton-2 run "+os.path.splitext(dalton_mol_filename)[0]))



