def fileHeader(): # fold>>
    return "***********  DALTON - An electronic structure program  ***********\n"
    # <<fold
def centerOfMass(): # fold>>
    return "Center-of-mass coordinates (A):    0.000000    1.000000    1.223609"
# <<fold 
def isotopicMasses(): # fold>>
    return """Isotopic Masses
                             ---------------

                           O1         15.994915
                           H1   1      1.007825
                           H1   2      1.007825
                           C1         12.000000
"""
# <<fold
def totalMass(): # fold>>
    return "Total mass:    30.010565 amu"
# <<fold 
def momentsOfInertia(): # fold>>
    return """Principal moments of inertia (u*A**2) and principal axes
 --------------------------------------------------------

   IA    1.747844          0.000000    0.000000    1.000000
   IB   13.208584          0.000000    1.000000    0.000000
   IC   14.956428          1.000000    0.000000    0.000000
"""
# <<fold 
def cartesianCoordinates(): # fold>>
    return """Cartesian Coordinates
  ---------------------

  Total number of coordinates: 12


   1   O1       x      0.0000000000
   2            y      0.0000000000
   3            z      0.3000000000

   4   H1   1   x      0.0000000000
   5            y     -1.7597098488
   6            z      3.3775957364

   7   H1   2   x      0.0000000000
   8            y      1.7597098488
   9            z      3.3775957364

  10   C1       x      0.0000000000
  11            y      0.0000000000
  12            z      2.3051919000
"""
# <<fold
def endOfOptimizationHeader(): # fold>>
    return "<<<<<<<<<<<<<<<<<<<<  End of Optimization  <<<<<<<<<<<<<<<<<<<<"
    # <<fold
def finalGeometryEnergy(): # fold>>
    return "Energy at final geometry is       :    -113.984888 a.u."
    # <<fold
def geometryConvergenceNumIterations(): # fold>>
    return "Geometry converged in            8  iterations!"
    # <<fold
def optimizationNextGeometry(): # fold>>
    return """Next geometry (au)
                            ------------------

 O1         0.0000000000            0.0000000000            0.0680928675
 H1   1     0.0000000000           -1.7554324515            3.4700805319
 H1   2     0.0000000000            1.7554324515            3.4700805319
 C1         0.0000000000            0.0000000000            2.3521294415

"""
# <<fold
def optimizationInfo(): # fold>>
    return """Optimization information
                         ------------------------

 Iteration number               :       0
 End of optimization            :       F 
 Energy at this geometry is     :    -113.932636
 Norm of gradient               :       0.567825
 Norm of step                   :       0.487002
 Updated trust radius           :       0.500000
 Total Hessian index            :       0
"""
# <<fold
def optimizationInfo2(): # fold>>
    return """Optimization information
                         ------------------------

 Iteration number               :       1
 End of optimization            :       T 
 Energy at this geometry is     :    -113.984495
 Energy change from last geom.  :      -0.051859
 Norm of gradient               :       0.030306
 Norm of step                   :       0.030552
 Updated trust radius           :       0.584403
 Total Hessian index            :       0
"""
# <<fold
def normalModesEigenvalues(): # fold>>
    return """Eigenvalues of mass-weighted Hessian
                    ------------------------------------
        
        
                Column   1     Column   2     Column   3     Column   4
        1     1.279649E-42   1.279649E-42   4.094095E-04   9.790871E-44
        
                Column   5     Column   6
        1     9.790871E-44  -1.212226E-21
"""
# <<fold
def normalModesEigenfunctions(): # fold>>
    return """Normal coordinates in Cartesian basis
                   -------------------------------------
        
        
                Column   1     Column   2     Column   3     Column   4
        1       0.02333068     0.00000000     0.00000000     0.00000000
        2       0.00000000     0.02333068     0.00000000     0.00000000
        3       0.00000000     0.00000000     0.02273544     0.00000000
        4       0.00000000     0.00000000     0.00000000     0.00537355
        6       0.00000000     0.00000000    -0.00120607     0.00000000
        
                Column   5     Column   6
        3       0.00000000     0.00523645
        5       0.00537355     0.00000000
        6       0.00000000     0.00523645
    """ 
# <<fold
def atomsAndBasisSetsTable(): # fold>>
    return """Atoms and basis sets
  --------------------

  Number of atom types:     2
  Total number of atoms:   10

  label    atoms   charge   prim    cont     basis
  ----------------------------------------------------------------------
  H1          1       1       7       5      [4s1p|2s1p]
  H2          1       1       7       5      [4s1p|2s1p]
  H3          1       1       7       5      [4s1p|2s1p]
  H4          1       1       7       5      [4s1p|2s1p]
  H5          1       1       7       5      [4s1p|2s1p]
  H6          1       1       7       5      [4s1p|2s1p]
  C1          1       6      26      14      [9s4p1d|3s2p1d]
  C2          1       6      26      14      [9s4p1d|3s2p1d]
  C3          1       6      26      14      [9s4p1d|3s2p1d]
  C4          1       6      26      14      [9s4p1d|3s2p1d]
  ----------------------------------------------------------------------
  total:     10      30     146      86
  ----------------------------------------------------------------------
  Spherical harmonic basis used.
"""
# <<fold
def dipoleMoment(): # fold>>

    return """Dipole moment
                              -------------

                    3.141592 au           0.000001 Debye
""" # <<fold

def dipoleMomentComponents(): # fold>>
    return """Dipole moment components
                         ------------------------

                               au             Debye

                    x      3.14159270      0.00000091
                    y     -1.23456789     -0.00000022
                    z      9.87654321      0.00000002
""" # <<fold

def HomoLumoSeparation(): # fold>>
    return """E(LUMO) :     0.01936070 au (symmetry 1)
          - E(HOMO) :    -0.28830940 au (symmetry 1)
            ------------------------------------------
                gap     :     0.30767010 au
""" # <<fold
def finalGeometry(): # fold>>

    return """Final geometry
                              --------------

 H1         0.0000002307           -0.0431166985           -0.0202403617
 H2         0.0000001751            1.6729220095           -3.0984614789
 H3        -0.0000000621            3.9834654382            2.2591198806
 H4        -0.0000004152            6.3971763363           -3.1312282876
 H5         0.0000000584            8.7077203406            2.2263528516
 H6         0.0000011485           10.4237584759           -0.8518686398
 C1         0.0000002040            1.7527241877           -1.0336061328
 C2        -0.0000000301            3.9601114154            0.1889860925
 C3        -0.0000005431            6.4205305038           -1.0610944968
 C4        -0.0000007662            8.6279178237            0.1614975188
""" # <<fold

def bondLengths(): # fold>>
    return """Bond distances (angstroms):
  ---------------------------

                  atom 1     atom 2       distance
                  ------     ------       --------
  bond distance:  C2   1     H1   1       1.091176
  bond distance:  C2   1     H3   1       1.093494
  bond distance:  C2   2     H1   2       1.091176
  bond distance:  C2   2     H3   2       1.093494
  bond distance:  C4   1     H5   1       1.095540
  bond distance:  C4   1     C2   1       1.335299
  bond distance:  C4   2     H5   2       1.095540
  bond distance:  C4   2     C2   2       1.335299
  bond distance:  C4   2     C4   1       1.460430
"""
  
# <<fold
def bondAngles(): # fold>>
    return """Bond angles (degrees):
  ----------------------

                  atom 1     atom 2     atom 3         angle
                  ------     ------     ------         -----
  bond angle:     H1   1     C2   1     H3   1       117.222
  bond angle:     H1   1     C2   1     C4   1       121.586
  bond angle:     H3   1     C2   1     C4   1       121.192
  bond angle:     H1   2     C2   2     H3   2       117.222
  bond angle:     H1   2     C2   2     C4   2       121.586
  bond angle:     H3   2     C2   2     C4   2       121.192
  bond angle:     H5   1     C4   1     C2   1       119.629
  bond angle:     H5   1     C4   1     C4   2       116.287
  bond angle:     C2   1     C4   1     C4   2       124.083
  bond angle:     H5   2     C4   2     C2   2       119.629
  bond angle:     H5   2     C4   2     C4   1       116.287
  bond angle:     C2   2     C4   2     C4   1       124.083
"""
# <<fold
