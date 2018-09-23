def commandDirective(): # fold>>
    return "# grrm/RHF/6-31+G*\n"
    # <<fold
def molecule(): # fold>>
    return """0 1
C          0.153400877033         -0.472050437678          0.397690014606
O          0.153399721839         -0.472050437678          1.533187825913
H         -0.355805044257         -1.354024025422         -1.436752410884
H          1.171818027261         -0.472050436090         -1.436750950354
"""
# <<fold
def optionsHeader(): # fold>>
    return "OPTIONS\n"
# <<fold
def nrunOption(): # fold>>
    return "nrun = 4\n"
# <<fold
