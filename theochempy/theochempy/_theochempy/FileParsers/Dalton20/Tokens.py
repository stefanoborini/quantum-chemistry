from theochempy._theochempy import Measure
from theochempy._theochempy import Units

import numpy
import re
import string

class FileHeaderToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("\*\*\*\*\*\*\*\*\*\*\*  DALTON - An electronic structure program  \*\*\*\*\*\*\*\*\*\*\*")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        reader.toPos(start_pos)
        return None 
        # <<fold

class CenterOfMassToken:
    def __init__(self, center_of_mass): #  fold>>
        self._center_of_mass = center_of_mass
        # <<fold
    def centerOfMass(self): # fold>>
        return self._center_of_mass
        # <<fold 
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("Center-of-mass coordinates \(A\):\s+(\d*\.\d*)\s+(\d*\.\d*)\s+(\d*\.\d*)", line)
        if m is not None:
            return cls( Measure.Measure( 
                                        (float(m.group(1)), 
                                         float(m.group(2)), 
                                         float(m.group(3))
                                        ), Units.bohr
                                        # WARNING: dalton 2.0 reports the center of mass as in angstrom, but the value is in bohr.
                                        # this is fixed in the dalton cvs.
                            )
                        )

        reader.toPos(start_pos)
        return None
    # <<fold

class TotalMassToken:
    def __init__(self, total_mass): #  fold>>
        self._total_mass = total_mass
    # <<fold
    def totalMass(self): # fold>>
        return self._total_mass
    # <<fold
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("Total mass:\s+(\d*\.\d*)", line)

        if m is not None:
            return cls( Measure.Measure(float(m.group(1)), Units.dalton))

        reader.toPos(start_pos)
        return None
    # <<fold

class IsotopicMassesToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()
        values = []

        line = reader.readline()
        m = re.search("Isotopic Masses", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        line = reader.readline()

        contents = False
        for line in reader:
            m = re.search("(\w+)\s+(\d+)\s+(\d*\.\d*)", line)
            if m is not None:
                values.append( (m.group(1), m.group(2), Measure.Measure( float(m.group(3)), Units.dalton)) )
                contents = True
                continue
    
            m = re.search("(\w+)\s+(\d*\.\d*)", line)
            if m is not None:
                values.append( (  m.group(1), "", Measure.Measure( float(m.group(2)), Units.dalton )) )
                contents = True
                continue
            break

        if contents == False:
            reader.toPos(start_pos)
            return None

        return cls(values)
    
    # <<fold 

class MomentsOfInertiaToken:
    def __init__(self, moments_of_inertia, principal_axes): # fold>>
        self._moments_of_inertia = moments_of_inertia
        self._principal_axes = principal_axes
    # <<fold
    def momentsOfInertia(self): # fold>>
        return self._moments_of_inertia
    # <<fold
    def principalAxes(self): # fold>>
        return self._principal_axes
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        moments_of_inertia = []
        principal_axes = []

        line = reader.readline()
        m = re.search("Principal moments of inertia", line)
        if m is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m=re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
        
        reader.readline()

        contents = False
        for line in reader:
            m = re.search("I.\s+(\d*\.\d*)\s+(\d*\.\d*)\s+(\d*\.\d*)\s+(\d*\.\d*)", line)
            if m is not None:
                moments_of_inertia.append( Measure.Measure( float(m.group(1)), Units.angstrom * Units.angstrom * Units.dalton) )
                principal_axes.append( Measure.Measure( 
                                                [float(m.group(2)), 
                                                 float(m.group(3)), 
                                                 float(m.group(4)),
                                                 ], Units.angstrom
                                        )
                                    )
                contents = True
                continue
            break

        if contents == False:
            reader.toPos(start_pos)
            return None

        return cls(moments_of_inertia, principal_axes)
    # <<fold

class CartesianCoordinatesToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()
        atom_list = []

        line = reader.readline()
        m = re.search("Cartesian Coordinates", line)
        if m is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        while True:
            line = reader.readline()
       
            if len(line.strip()) != 0:
                break
            if reader.isAtEOF():
                return None
        
        m0 = re.search("Total number of coordinates:\s*(\d+)", line)
        if m0 is None:
            return None

        while True:
            line = reader.readline()
        
            if len(line.strip()) != 0:
                break
            if reader.isAtEOF():
                return None



        valid_data = True
       
        while True:
            m1 = re.search("\s+\d+\s+(\w+)\s+(\w+)\s+x\s+(-?\d+\.\d+)", line)
            m2 = re.search("\s+\d+\s+(\w+)\s+x\s+(-?\d+\.\d+)", line)

            if m1 is None and m2 is None:
                break
            elif m1 is not None:
                label = m1.group(1)
                sym_label = m1.group(2)
                x_coord = float(m1.group(3))
            elif m2 is not None:
                label = m2.group(1)
                sym_label = ""
                x_coord = float(m2.group(2))
           
            line = reader.readline()
            m3 = re.search("^\s+\d+\s+y\s*(-?\d+\.\d+)",line)

            if m3 is None:
                valid_data = False
                break

            y_coord = float(m3.group(1))

            line = reader.readline()
            m4 = re.search("^\s+\d+\s+z\s*(-?\d+\.\d+)", line)

            if m4 is None:
                valid_data = False    
                break
            z_coord = float(m4.group(1))

            atom_list.append( (label, sym_label, Measure.Measure ( (x_coord, y_coord, z_coord), Units.bohr) ))

            line = reader.skipLines(2)

        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            reader.toPos(start_pos)
            return None

        return cls(atom_list)

    
    # <<fold 

class EndOfOptimizationHeaderToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("<<<<<<<<<<<<<<<<<<<<  End of Optimization  <<<<<<<<<<<<<<<<<<<<")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        reader.toPos(start_pos)
        return None 
        # <<fold

class FinalGeometryEnergyToken:
    def __init__(self, energy): # fold>>
        self._energy = energy
    # <<fold 
    def energy(self): # fold>>
        return self._energy
    # <<fold
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        m = re.search("Energy at final geometry is\s+:\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( Measure.Measure(float(m.group(1)), Units.hartree))

        reader.toPos(start_pos)
        return None
    # <<fold

class GeometryConvergenceNumIterationsToken:
    def __init__(self, iterations): # fold>>
        self._iterations = iterations
    # <<fold 
    def iterations(self): # fold>>
        return self._iterations
    # <<fold
    @classmethod
    def match(cls, reader):  # fold>>
        start_pos = reader.currentPos()
        line = reader.readline()
        
        m = re.search("Geometry converged in\s+(\d+)\s+iteration", line)
        if m is not None:
            try:
                iterations = int(m.group(1))
            except ValueError:
                reader.toPos(start_pos)
                return None
             
            return cls(iterations)

        reader.toPos(start_pos)
        return None
    # <<fold

class OptimizationNextGeometryToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()
        atom_list = []

        line = reader.readline()
        m = re.search("Next geometry", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        reader.readline()

        valid_data = False

        for line in reader:
            m1 = re.search("\s+(\w+)\s+(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m1 is not None:
                atom_label = m1.group(1)
                sym_label = m1.group(2)
                position = Measure.Measure( (float(m1.group(3)),
                                             float(m1.group(4)),
                                             float(m1.group(5))
                                             ), Units.bohr
                                            )
                atom_list.append( (atom_label, sym_label, position) )
                valid_data = True
                continue

            m2 = re.search("\s+(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m2 is not None:
                atom_label = m2.group(1)
                sym_label = ""
                position = Measure.Measure ( (float(m2.group(2)),
                                              float(m2.group(3)),
                                              float(m2.group(4))
                                              ) , Units.bohr
                                            )

                atom_list.append( (atom_label, sym_label, position))
                valid_data = True
                continue

            break

        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            reader.toPos(start_pos)
            return None

        return cls(atom_list)

    # <<fold 

class OptimizationInfoToken:
    def __init__(self, iteration, end_of_optimization, energy, energy_change, gradient_norm, step_norm, trust_radius, total_hessian_index): # fold>>
        self._iteration = iteration
        self._end_of_optimization = end_of_optimization
        self._energy = energy
        self._energy_change = energy_change
        self._gradient_norm = gradient_norm
        self._step_norm = step_norm
        self._trust_radius = trust_radius
        self._total_hessian_index = total_hessian_index
    # <<fold 
    def iteration(self): # fold>>
        return self._iteration
        # <<fold
    def endOfOptimization(self): # fold>>
        return self._end_of_optimization
        # <<fold
    def energy(self): # fold>>
        return self._energy
        # <<fold
    def energyChange(self): # fold>>
        return self._energy_change
        # <<fold
    def gradientNorm(self): # fold>>
        return self._gradient_norm
        # <<fold
    def stepNorm(self): # fold>>
        return self._step_norm
        # <<fold
    def trustRadius(self): # fold>>
        return self._trust_radius
        # <<fold
    def totalHessianIndex(self): # fold>>
        return self._total_hessian_index
        # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m = re.search("Optimization information", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        reader.readline()

        line = reader.readline()
        m1 = re.search("Iteration number\s+:\s+(\d+)", line)
        if m1 is not None:
            try:
                iteration = int(m1.group(1))
            except ValueError:
                reader.toPos(start_pos)
                return None
        else:
            reader.toPos(start_pos)
            return None
        
        line = reader.readline()
        m2 = re.search("End of optimization\s+:\s+([TF])", line)
        if m2 is not None:
            if m2.group(1) == "T":
                end_of_optimization = True
            else:
                end_of_optimization = False
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m3 = re.search("Energy at this geometry is\s+:\s+(-?\d*\.\d*)", line)
        if m3 is not None:
            energy = Measure.Measure(float(m3.group(1)), Units.hartree)
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m4 = re.search("Energy change from last geom\.\s+:\s+(-?\d*\.\d*)", line)
        if m4 is not None:
            energy_change = Measure.Measure(float(m4.group(1)), Units.hartree)
        else:
            energy_change = None
            reader.readbackline()

        line = reader.readline()
        m5 = re.search("Norm of gradient\s+:\s+(-?\d*\.\d*)", line)
        if m5 is not None:
            gradient_norm = Measure.Measure( float(m5.group(1)), Units.unknown)
        else:
            reader.toPos(start_pos)
            return None
        
        line = reader.readline()
        m6 = re.search("Norm of step\s+:\s+(-?\d*\.\d*)", line)
        if m6 is not None:
            step_norm = Measure.Measure( float(m6.group(1)), Units.unknown)
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m7 = re.search("Updated trust radius\s+:\s+(-?\d*\.\d*)", line)
        if m7 is not None:
            trust_radius = Measure.Measure( float(m7.group(1)), Units.unknown)
        else:
            reader.toPos(start_pos)
            return None
        
        line = reader.readline()
        m8 = re.search("Total Hessian index\s+:\s+(\d*)", line)
        if m8 is not None:
            try:
                total_hessian_index = int(m8.group(1))
            except ValueError:
                reader.toPos(start_pos)
                return None
        else:
            reader.toPos(start_pos)
            return None
            
        return cls(iteration, end_of_optimization, energy, energy_change, gradient_norm, step_norm, trust_radius, total_hessian_index)

    # <<fold 

class NormalModesEigenvaluesToken:
    def __init__(self, values): # fold>>
        self._values = values
        # <<fold
    def values(self):  # fold>>
        return self._values
        # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        values= []

        line = reader.readline()
        m = re.search("Eigenvalues of mass-weighted Hessian", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
      
        reader.skipLines(2)

        all_columns = []
        all_values = []
        unknown_marker_reached = True
        while True:
            line = reader.readline()
            column_numbers = _tryReadColumnHeader(line)
            if column_numbers is not None:
                unknown_marker_reached = False
                all_columns.extend(column_numbers)
                continue

            values_tuple = _tryReadRowValues(line)
            if values_tuple is not None:
                index, values = values_tuple
                unknown_marker_reached = False
                all_values.extend(map(float,values))
                continue

            if unknown_marker_reached == True:
                # twice an unknown marker is enough to bail out
                break
            unknown_marker_reached=True 
            
        if len(all_columns) == 0 or len(all_values) == 0:
            return None

        output = [None]*max(all_columns)
        for index, value in zip(all_columns, all_values):
            output[index-1] = Measure.Measure(value, Units.unknown)
      
        if None in output:
            return None

        return cls(output)
        # <<fold
def _tryReadColumnHeader(line): # fold>>
   
    # first, match the whole group repetition

    m = re.match("^\s*(Column\s+\d+\s*)+\s*$", line)
    if m is None:
        return None
   
    column_header_re = "Column\s+(\d+)"
    values = [] 
    for m in re.finditer(column_header_re, line):
        values.append(int(m.group(1)))

    return values
    # <<fold
def _tryReadRowValues(line): # fold>>
    m = re.match("^\s*(\d+)\s+(-?\d\.\d+[DdEe][+-]\d\d\s*)+\s*$", line)
    if m is None:
        return None

    # extract the index
    re.search("\s(\d+)\s+(-?\d\.\d+[DdEe][+-]\d\d)\s+", line)
    index = int(m.group(1))
    values = []
    
    for m in re.finditer("(-?\d\.\d+[DdEe][+-]\d\d)", line):
        transl=string.maketrans('dD','ee')
        values.append(float(string.translate(m.group(1), transl)))

    return (index, values)
    # <<fold 
        
class AtomsAndBasisSetsToken:
    def __init__(self, num_atom_types, num_tot_atoms, atom_data_list, total_atom_data, spherical, basis_set): # fold>>
        self._num_atom_types = num_atom_types
        self._num_tot_atoms = num_tot_atoms
        self._atom_data_list = atom_data_list
        self._total_atom_data = total_atom_data
        self._spherical = spherical
        self._basis_set = basis_set
    # <<fold 
    def numOfAtomTypes(self): # fold>>
        return self._num_atom_types
    # <<fold
    def totalNumberOfAtoms(self): # fold>>
        return self._num_tot_atoms
    # <<fold
    def atomDataList(self): # fold>>
        return self._atom_data_list
        # <<fold
    def totalAtomData(self): # fold>>
        return self._total_atom_data
        # <<fold
    def spherical(self): # fold>>
        return self._spherical
    # <<fold
    def basisSet(self): # fold>>
        return self._basis_set
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m = re.search("Atoms and basis sets", line)
        if m is None:
            reader.toPos(start_pos)
            return None

        reader.skipLines(2)

        line = reader.readline()
        m1 = re.search("Number of atom types:\s*([0-9]+)", line)
        if m1 is not None:
            try:
                num_atom_types = int(m1.group(1))
            except ValueError:
                reader.toPos(start_pos)
                return None
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m2 = re.search("Total number of atoms:\s*([0-9]+)", line)
        if m2 is not None:
            try:
                num_tot_atoms = int(m2.group(1))
            except ValueError:
                reader.toPos(start_pos)
                return None
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        line = reader.readline()
        m2_1 = re.search("Basis set used is \"(.*?)\" from the basis set library\.", line)
        if m2_1 is not None:
            basis_set = m2_1.group(1)
            reader.skipLines(2)
        else:
            basis_set = None
            
        line = reader.readline()
        atom_data_list = []
        regexp=re.compile("^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\[.*\])\s+")
        # example line
        #  O1          1       8      42      30      [10s5p2d1f|4s3p2d1f]
        while True:
            line = reader.readline()
            m3 = regexp.match(line)
            if m3 is None:
                break
            label = m3.group(1)
            try:
                atoms = int(m3.group(2))
                charge = int(m3.group(3))
                primitives = int(m3.group(4))
                contracted = int(m3.group(5))
            except ValueError:
                reader.toPos(start_pos)
                return None
            basis = m3.group(6)
            atom_data_list.append( (label, atoms, charge, primitives, contracted, basis) ) 

        line = reader.readline()
        m4 = re.search("total:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
        if m4 is None:
            reader.toPos(start_pos)
            return None
        total_atoms = m4.group(1)
        total_charge = m4.group(2)
        total_primitives = m4.group(3)
        total_contracted = m4.group(4)

        total_atom_data = ( total_atoms, total_charge, total_primitives, total_contracted)

        reader.readline()
        
        line = reader.readline()

        m5 = re.search("Spherical harmonic basis used", line)
        if m5 is None:
            spherical = False
        else:
            spherical = True
            
        return cls( num_atom_types, num_tot_atoms, atom_data_list, total_atom_data, spherical, basis_set)
    # <<fold 

class FinalGeometryToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()
        atom_list = []

        line = reader.readline()
        m = re.search("Final geometry", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        reader.readline()

        valid_data = False

        for line in reader:
            m1 = re.search("\s+(\w+)\s+(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m1 is not None:
                position = Measure.Measure( (float(m1.group(3)), float(m1.group(4)), float(m1.group(5))), Units.bohr )
                atom_list.append( (m1.group(1), m1.group(2), position))
                valid_data = True
                continue

            m2 = re.search("\s+(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m2 is not None:
                position = Measure.Measure( ( float(m2.group(2)), 
                                              float(m2.group(3)), 
                                              float(m2.group(4))
                                            ), Units.bohr)
                atom_list.append( (m2.group(1), "", position))
                valid_data = True
                continue

            break

        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            reader.toPos(start_pos)
            return None

        return cls(atom_list)

    # <<fold 
 
class DipoleMomentToken:
    def __init__(self, dipole): # fold>>
        self._dipole= dipole
    # <<fold 
    def dipole(self): # fold>>
        return self._dipole
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m = re.search("Dipole moment", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        reader.readline()

        valid_data = False

        line = reader.readline()
        m1 = re.search("\s+(-?\d+\.\d+)\s+au\s+(-?\d+\.\d+)\s+Debye", line)

        if m1 is None:
            reader.toPos(start_pos)
            return None

        try:
            dipole = Measure.Measure(float(m1.group(2)), Units.debye)
        except ValueError:
            reader.toPos(start_pos)
            return None

        return cls(dipole)

    # <<fold 

class DipoleMomentComponentsToken:
    def __init__(self, dipole): # fold>>
        self._dipole= dipole
    # <<fold 
    def dipole(self): # fold>>
        return self._dipole
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m = re.search("Dipole moment components", line)
        if m is None:
            reader.toPos(start_pos)
            return None
    
        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None
       
        reader.skipLines(3)

        line1= reader.readline()
        line2= reader.readline()
        line3= reader.readline()
        m1 = re.search("\s+x\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+", line1)
        m2 = re.search("\s+y\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+", line2)
        m3 = re.search("\s+z\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+", line3)

        if m1 is None or m2 is None or m3 is None:
            reader.toPos(start_pos)
            return None

        try:
            dipole_x = float(m1.group(2))
            dipole_y = float(m2.group(2))
            dipole_z = float(m3.group(2))
        except ValueError:
            reader.toPos(start_pos)
            return None

        return cls(Measure.Measure([dipole_x, dipole_y, dipole_z], Units.debye))

    # <<fold 
 
class HOMOLUMOSeparationToken:
    def __init__(self, homo_energy, homo_symmetry, lumo_energy, lumo_symmetry, gap): # fold>>
        self._homo_energy = homo_energy
        self._lumo_energy = lumo_energy
        self._homo_symmetry = homo_symmetry
        self._lumo_symmetry = lumo_symmetry
        self._gap = gap
    # <<fold 
    def gap(self): # fold>>
        return self._gap
    # <<fold
    def HOMOEnergy(self): # fold>>
        return self._homo_energy
    # <<fold
    def HOMOSymmetry(self): # fold>>
        return self._homo_symmetry
    # <<fold
    def LUMOEnergy(self): # fold>>
        return self._lumo_energy
    # <<fold
    def LUMOSymmetry(self): # fold>>
        return self._lumo_symmetry
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()

        line = reader.readline()
        m1 = re.search("E\(LUMO\)\s:\s+(-?\d+\.\d+)\s+au\s+\(symmetry (\d+)\)", line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m2 = re.search("-\s+E\(HOMO\)\s:\s+(-?\d+\.\d+)\s+au\s+\(symmetry (\d+)\)", line)
        if m2 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()

        line = reader.readline()
        m3 = re.search("gap\s+:\s+(-?\d+\.\d+)\s+au\s+", line)
        if m3 is None:
            reader.toPos(start_pos)
            return None
       
        try:
            lumo_energy = Measure.Measure(float(m1.group(1)), Units.hartree)
            lumo_symmetry = int(m1.group(2))
            homo_energy = Measure.Measure(float(m2.group(1)), Units.hartree)
            homo_symmetry = int(m2.group(2))
            gap = Measure.Measure(float(m3.group(1)), Units.hartree)
        except ValueError:
            reader.toPos(start_pos)
            return None

        return cls(homo_energy, homo_symmetry, lumo_energy, lumo_symmetry, gap)

    # <<fold 

class BondLengthsToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m1 = re.search("Bond distances\s\(angstroms\):", line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m2 = re.search("-+", line)
        if m2 is None:
            reader.toPos(start_pos)
            return None

        # read empty line
        line = reader.readline()

        line = reader.readline()
        m3 = re.search("\s+atom 1\s+atom 2\s+distance", line)
        if m3 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m4 = re.search("-+\s+-+\s+-+", line)
        if m4 is None:
            reader.toPos(start_pos)
            return None

        atom_list = []
        valid_data=False
        for line in reader:
            # symmetry labels in both atoms
            m5 = re.search("bond distance:\s+(\w+)\s+(\d)\s+(\w+)\s+(\d)\s+(\d+\.\d+)", line)
            if m5 is not None:
                atom_list.append( ( (m5.group(1), m5.group(2)) , (m5.group(3), m5.group(4)) ,  Measure.Measure(float(m5.group(5)), Units.angstrom) ) )
                valid_data = True
                continue

            # symmetry label only on left atom
            m6 = re.search("bond distance:\s+(\w+)\s+(\d)\s+(\w+)\s+(\d+\.\d+)", line)
            if m6 is not None:
                atom_list.append( ( (m6.group(1), m6.group(2)) , (m6.group(3), "") ,  Measure.Measure(float(m6.group(4)), Units.angstrom) ) )
                valid_data = True
                continue

            # symmetry labels only on right atom
            m7 = re.search("bond distance:\s+(\w+)\s+(\w+)\s+(\d)\s+(\d+\.\d+)", line)
            if m7 is not None:
                atom_list.append( ( (m7.group(1), "") , (m7.group(2), m7.group(3)) ,  Measure.Measure(float(m7.group(4)), Units.angstrom) ) )
                valid_data = True
                continue

            # symmetry labels on no atoms
            m8 = re.search("bond distance:\s+(\w+)\s+(\w+)\s+(\d+\.\d+)", line)
            if m8 is not None:
                atom_list.append( ( (m8.group(1), "") , (m8.group(2), "") ,  Measure.Measure( float(m8.group(3)), Units.angstrom) ) )
                valid_data = True
                continue

            break

        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            reader.toPos(start_pos)
            return None

        return cls(atom_list)

    # <<fold 

class SymmetryToken:
    def __init__(self, generators): # fold>>
        self._generators = generators
        # <<fold
    def generators(self): # fold>>
        return self._generators
        # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m1 = re.search("SYMGRP:Point group information", line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m2 = re.search("-+", line)
        if m2 is None:
            reader.toPos(start_pos)
            return None

        # read empty line
        line = reader.readline()

        line = reader.readline()
        m3 = re.search("Full group is:", line)
        m3_1 = re.search("Point group:", line)

        if m3 is None and m3_1 is None:
            reader.toPos(start_pos)
            return None

        if m3 is not None:
            line = reader.readline()
            m4 = re.search("Represented as:", line)
            if m4 is None:
                reader.toPos(start_pos)
                return None

        # read empty line
        line = reader.readline()

        line = reader.readline()
        m5 = re.search("\* The point group was generated by:", line)
        if m5 is None:
            return cls([])

        # read empty line
        line = reader.readline()

        generators = []
        line = reader.readline()
        while len(line.strip()) != 0:
            if line.strip() == "Reflection in the xy-plane":
                generators.append("Z")
            elif line.strip() == "Reflection in the xz-plane":
                generators.append("Y")
            elif line.strip() == "Reflection in the yz-plane":
                generators.append("X")
            elif line.strip() == "Rotation about the x-axis":
                generators.append("YZ")
            elif line.strip() == "Rotation about the y-axis":
                generators.append("XZ")
            elif line.strip() == "Rotation about the z-axis":
                generators.append("XY")
            elif line.strip() == "Inversion centre":
                generators.append("XYZ")
            else:
                reader.toPos(start_pos)
                return None
            line = reader.readline()

        return cls(generators)
        # <<fold

class ResponseHeaderToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp = re.compile("This is output from RESPONSE  -  an MCSCF and SOPPA response property program")
        line = reader.readline()
        m1 = regexp.search(line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m = re.search("-*", line)
        if m is None:
            reader.toPos(start_pos)
            return None


        return cls()
        # <<fold

class FirstHyperpolarizabilityComponentToken:
    def __init__(self, b_freq, c_freq, components, beta, refers_to): # fold>>
        self._b_freq = b_freq
        self._c_freq = c_freq
        self._components = components
        self._beta = beta
        self._refers_to = refers_to
        pass
    # <<fold
    def BFreq(self):
        return self._b_freq
    def CFreq(self):
        return self._c_freq
    def components(self):
        return self._components
    def beta(self):
        return self._beta
    def refersTo(self):
        return self._refers_to
    @classmethod
    def match(cls, reader): # fold>>
        start_pos = reader.currentPos()
        regexp1 = re.compile("@\s+B-freq\s+=\s+(\d+\.\d+)\s+C-freq\s+=\s+(\d+\.\d+)\s+beta\(([XYZ]);([XYZ]),([XYZ])\)\s+=\s*(-?\d+\.\d+)")
        regexp2 = re.compile("@\s+B-freq\s+=\s+(\d+\.\d+)\s+C-freq\s+=\s+(\d+\.\d+)\s+beta\(([XYZ]);([XYZ]),([XYZ])\)\s+=\s+beta\(([XYZ]),([XYZ]),([XYZ])\)")
        line = reader.readline()
        m1 = regexp1.search(line)
        m2 = regexp2.search(line)

        if m1 is not None:
            b_freq = Measure.Measure(float(m1.group(1)), Units.frequency_au)
            c_freq = Measure.Measure(float(m1.group(2)), Units.frequency_au)
            components = (m1.group(3), m1.group(4), m1.group(5))
            beta = Measure.Measure(float(m1.group(6)), Units.beta_au)
            refers_to = None
        elif m2 is not None:
            b_freq = Measure.Measure(float(m2.group(1)), Units.frequency_au)
            c_freq = Measure.Measure(float(m2.group(2)), Units.frequency_au)
            components = (m2.group(3), m2.group(4), m2.group(5))
            beta = None
            refers_to = (m2.group(6), m2.group(7), m2.group(8))
        else:
            reader.toPos(start_pos)
            return None

        return cls(b_freq, c_freq, components, beta, refers_to)
    # <<fold

class SecondHyperpolarizabilityToken:
    def __init__(self, b_freq, c_freq, d_freq, gamma, averaged_gamma): # fold>>
        self._b_freq = b_freq
        self._c_freq = c_freq
        self._d_freq = d_freq
        self._gamma = gamma
        self._averaged_gamma = averaged_gamma
    # <<fold
    def BFreq(self):
        return self._b_freq
    def CFreq(self):
        return self._c_freq
    def DFreq(self):
        return self._d_freq
    def gamma(self, A, B, C, D):
        try:
            return self._gamma[ (A,B,C,D) ]
        except KeyError:
            return None
    def allGamma(self):
        return self._gamma
    def averagedGamma(self):
        return self._averaged_gamma
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m1 = re.search("Summary of gamma values for a set of frequencies", line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m2 = re.search("-+", line)
        if m2 is None:
            reader.toPos(start_pos)
            return None

        # read empty line
        line = reader.readline()


        line = reader.readline()
        m3 = re.search("@ B-freq:\s+(\d+\.\d+)", line)
        if m3 is None:
            reader.toPos(start_pos)
            return None
     
        b_freq = Measure.Measure(float(m3.group(1)), Units.frequency_au)

        line = reader.readline()
        m4 = re.search("@ C-freq:\s+(\d+\.\d+)", line)
        if m4 is None:
            reader.toPos(start_pos)
            return None

        c_freq = Measure.Measure(float(m4.group(1)), Units.frequency_au)

        line = reader.readline()
        m5 = re.search("@ D-freq:\s+(\d+\.\d+)", line)
        if m5 is None:
            reader.toPos(start_pos)
            return None

        d_freq = Measure.Measure(float(m5.group(1)), Units.frequency_au)

        # skip empty line
        line = reader.readline()

        gamma = {}
        valid_data=False
        for line in reader:
            # symmetry labels in both atoms
            m6 = re.search("@ gamma\(([XYZ]);([XYZ]),([XYZ]),([XYZ])\)\s+(-?\d+\.\d+)", line)
            if m6 is not None:
                gamma[ (m6.group(1), m6.group(2), m6.group(3), m6.group(4)) ] = Measure.Measure(float(m6.group(5)), Units.gamma_au)
                valid_data = True
                continue
            break
    
        # line already skipped by the loop

        line = reader.readline()
        m7 = re.search("@ Averaged gamma parallel to the applied field is\s+(-?\d+\.\d+)", line)
        if m7 is not None:
            averaged_gamma = Measure.Measure(float(m7.group(1)), Units.gamma_au)
        else:
            averaged_gamma = None

        return cls(b_freq, c_freq, d_freq, gamma, averaged_gamma)
    # <<fold

class LinearResponseToken:
    def __init__(self, a_freq, b_freq, components, alpha): # fold>>
        self._a_freq = a_freq
        self._b_freq = b_freq
        self._alpha = alpha
        self._components = components
    # <<fold
    def AFreq(self):
        return self._a_freq
    def BFreq(self):
        return self._b_freq
    def alpha(self):
        return self._alpha
    def components(self):
        return self._components
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m1 = re.search("@ Singlet linear response function in a.u.", line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        # read empty line
        line = reader.readline()

        line = reader.readline()
        m3 = re.search("@ A operator, symmetry, frequency:\s+(\w+)\s+(\d)\s+(-?\d+\.\d+)", line)
        if m3 is None:
            reader.toPos(start_pos)
            return None
     
        a_freq = Measure.Measure(float(m3.group(3)), Units.frequency_au)
        if m3.group(1) == "XDIPLEN":
            a_component = "X"
        elif m3.group(1) == "YDIPLEN":
            a_component = "Y"
        elif m3.group(1) == "ZDIPLEN":
            a_component = "Z"
        else:
            a_component = None

        line = reader.readline()
        m4 = re.search("@ B operator, symmetry, frequency:\s+(\w+)\s+(\d)\s+(-?\d+\.\d+)", line)
        if m4 is None:
            reader.toPos(start_pos)
            return None

        b_freq = Measure.Measure(float(m4.group(3)), Units.frequency_au)
        if m4.group(1) == "XDIPLEN":
            b_component = "X"
        elif m4.group(1) == "YDIPLEN":
            b_component = "Y"
        elif m4.group(1) == "ZDIPLEN":
            b_component = "Z"
        else:
            b_component = None

        # read empty line
        line = reader.readline()

        line = reader.readline()
        m5 = re.search("@ Value of linear response -<<A;B>\(omega\):\s+(-?\d+\.\d+)", line)
        if m5 is None:
            reader.toPos(start_pos)
            return None

        alpha = Measure.Measure(float(m5.group(1)), Units.alpha_au)

        return cls(a_freq, b_freq, [a_component, b_component], alpha)
    # <<fold




class SevereErrorToken:
    def __init__(self, reason): # fold>>
        self._reason = reason
    # <<fold
    def reason(self): # fold>>
        return self._reason
    # <<fold
    @classmethod
    def match(cls, reader): # fold>>

        start_pos = reader.currentPos()

        line = reader.readline()
        m1 = re.search("--- SEVERE ERROR, PROGRAM WILL BE ABORTED ---", line)
        if m1 is None:
            reader.toPos(start_pos)
            return None

        # skip lines with date, time and hostname, and a blank line
        line = reader.readline()
        line = reader.readline()
        line = reader.readline()

        # get the reason
        line = reader.readline()

        m2 = re.search("Reason: (.*)", line)
        if m2 is None:
            reader.toPos(start_pos)
            return None

        reason = m2.group(1)
        return cls(reason)
    # <<fold

def fullGrammar():
    token_grammar=[ 
            FileHeaderToken,
            CenterOfMassToken,
            IsotopicMassesToken,
            TotalMassToken,
            MomentsOfInertiaToken,
            CartesianCoordinatesToken,
            EndOfOptimizationHeaderToken,
            FinalGeometryEnergyToken,
            GeometryConvergenceNumIterationsToken,
            OptimizationNextGeometryToken,
            OptimizationInfoToken,
            NormalModesEigenvaluesToken,
            AtomsAndBasisSetsToken,
            DipoleMomentToken,
            DipoleMomentComponentsToken,
            FinalGeometryToken,
            HOMOLUMOSeparationToken,
            BondLengthsToken,
            SymmetryToken,
            ResponseHeaderToken,
            FirstHyperpolarizabilityComponentToken,
            SecondHyperpolarizabilityToken,
            LinearResponseToken,
            SevereErrorToken,
            ] 
    return token_grammar


