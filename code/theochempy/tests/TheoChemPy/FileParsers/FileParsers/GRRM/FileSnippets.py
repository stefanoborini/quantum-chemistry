def headerDissociated(): # fold>>
    return "List of Dissociated Structures\n"
    # <<fold
def headerEquilibrium(): # fold>>
    return "List of Equilibrium Structures\n"
    # <<fold
def headerTransition(): # fold>>
    return "List of Transition Structures\n"
    # <<fold
def structureHeader(): # fold>>
    return "# Geometry of DC 1, SYMMETRY = C1\n"
# <<fold 
def geometry(): # fold>>
    return """C     -1.278867383494  -0.318231568940  -0.480462668395
C      0.032850345193  -0.731571903696   0.068502440746
O      1.082403177555   0.054618071399  -0.377296013005
H      0.939622192877   0.951018247769  -0.090855229968
H     -1.330524520394   0.132634440401  -1.449468626090
H      0.214263476185  -1.739501177711  -0.311619324337
H     -2.187016042103  -0.691216603882  -0.050675545236
H     -0.011644460012  -0.799847759845   1.148735850746
H     -1.620767160853   2.166984411459   0.595515448078
"""
# <<fold
def energy(): # fold>>
    return "Energy    = -153.869550889154\n"
# <<fold
def spin(): # fold>>
    return "Spin(**2) =    0.000000000000\n"
# <<fold
def zpve(): # fold>>
    return "ZPVE      =    0.074920061481\n"
# <<fold
def normalModes(): # fold>>
    return """Normal mode eigenvalues : nmode = 20
  0.005095752   0.007573452   0.010127638   0.011522505   0.016905850
  0.027532224   0.035258968   0.046415246   0.054120725   0.060140403
  0.064624340   0.085378679   0.088983920   0.098167720   0.099022562
  0.377086524   0.402913199   0.437531319   0.469693252   0.617328982
"""
# <<fold
def connection(): # fold>>
    return "CONNECTION : 0 - DC\n"

# <<fold
def dissociationFragments(): # fold>>
    return """Dissociation fragments : nfrag = 2
CO / H2
# DF 0 = { 1,  2}
# DF 1 = { 3,  4}
"""

# <<fold
