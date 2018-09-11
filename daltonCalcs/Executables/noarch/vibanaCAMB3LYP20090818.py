#/usr/bin/env python
# @author Stefano Borini
# @description this script computes the vibrational analysis
# @license Artistic License 2.0

import getopt
import os
import sys

def _usage():
    print "Usage : "+os.path.basename(sys.argv[0])
    print ""
    print "Computes the vibrational analysis for a given dalton file"
    print ""
    print ""

if len(sys.argv[1:]) < 1:
    _usage()
    sys.exit(1)

dalton_mol_filename = sys.argv[1]

f = file(os.path.join(os.getcwd(),"run.dal"),"w")
f.write("""# this file generated automatically by vibanaCAMB3LYP20090818.py
**DALTON
.RUN PROPERTIES
.DIRECT
**INTEGRALS
.NOSUP
*END OF HERMIT
**WAVE FUNCTIONS
.DFT
CAMB3LYP
**PROPERTIES
.VIBANA
*END OF
""")
f.close()

sys.exit(os.system("cnrun dalton-2 run "+os.path.splitext(dalton_mol_filename)[0]))
