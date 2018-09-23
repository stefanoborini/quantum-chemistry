#!/bin/bash
execute="$PACKAGE_ROOT_DIR/Executables/noarch/polyacetylenes_$1-$2_subst_generator.py"
if test -e $execute
then
    python $execute $3
    exit $?
fi

cat <<EOF
Usage: `basename $0` end-chain-1 end-chain-2 num_repetitions

Script that generates polyacetylenes in a format suitable for the script zmat2input in
TheoChemPy. The number of repetition is the amount of repetitions of the central H-C=C-H
unit.
EOF
