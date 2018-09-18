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
        m = re.search("Center-of-mass coordinates.*?:\s+(\d*\.\d*)\s+(\d*\.\d*)\s+(\d*\.\d*)", line)
        if m is not None:
            return cls( (m.group(1), m.group(2), m.group(3)))

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
            return cls(m.group(1))

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
                values.append( (m.group(1), m.group(2), m.group(3)))
                contents = True
                continue
    
            m = re.search("(\w+)\s+(\d*\.\d*)", line)
            if m is not None:
                values.append( (  m.group(1), "", m.group(2)))
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
        principal_axes = [[],[],[]]

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
                moments_of_inertia.append(m.group(1))
                principal_axes[len(moments_of_inertia)-1].extend([m.group(2), m.group(3), m.group(4)])
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
       
        reader.skipLines(4)

        valid_data = True

        line = reader.readline()
        while True:
            m1 = re.search("\s+\d+\s+(\w+)\s+(\w+)\s+x\s+(-?\d+\.\d+)", line)
            m2 = re.search("\s+\d+\s+(\w+)\s+x\s+(-?\d+\.\d+)", line)
            
            if m1 is None and m2 is None:
                break
            elif m1 is not None:
                label = m1.group(1)
                sym_label = m1.group(2)
                x_coord = m1.group(3)
            elif m2 is not None:
                label = m2.group(1)
                sym_label = ""
                x_coord = m2.group(2)
           
            line = reader.readline()
            m3 = re.search("^\s+\d+\s+y\s*(-?\d+\.\d+)",line)

            if m3 is None:
                valid_data = False
                break

            y_coord = m3.group(1)

            line = reader.readline()
            m4 = re.search("^\s+\d+\s+z\s*(-?\d+\.\d+)", line)

            if m4 is None:
                valid_data = False    
                break
            z_coord = m4.group(1)

            atom_list.append( (label, sym_label, (x_coord, y_coord, z_coord) ))

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
            return cls(m.group(1))

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
                atom_list.append( (m1.group(1), m1.group(2), (m1.group(3), m1.group(4), m1.group(5))))
                valid_data = True
                continue

            m2 = re.search("\s+(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m2 is not None:
                atom_list.append( (m2.group(1), "", (m2.group(2), m2.group(3), m2.group(4))))
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
            energy = m3.group(1)
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m4 = re.search("Energy change from last geom\.\s+:\s+(-?\d*\.\d*)", line)
        if m4 is not None:
            energy_change = m4.group(1)
        else:
            energy_change = None
            reader.readbackline()

        line = reader.readline()
        m5 = re.search("Norm of gradient\s+:\s+(-?\d*\.\d*)", line)
        if m5 is not None:
            gradient_norm = m5.group(1)
        else:
            reader.toPos(start_pos)
            return None
        
        line = reader.readline()
        m6 = re.search("Norm of step\s+:\s+(-?\d*\.\d*)", line)
        if m6 is not None:
            step_norm = m6.group(1)
        else:
            reader.toPos(start_pos)
            return None

        line = reader.readline()
        m7 = re.search("Updated trust radius\s+:\s+(-?\d*\.\d*)", line)
        if m7 is not None:
            trust_radius = m7.group(1)
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
            output[index-1] = value
      
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
    def __init__(self, num_atom_types, num_tot_atoms, atom_data_list, total_atom_data, spherical): # fold>>
        self._num_atom_types = num_atom_types
        self._num_tot_atoms = num_tot_atoms
        self._atom_data_list = atom_data_list
        self._total_atom_data = total_atom_data
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


        #  O1          1       8      42      30      [10s5p2d1f|4s3p2d1f]
        reader.skipLines(3)

        atom_data_list = []
        regexp=re.compile("^\s*(\w+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\[.*\])\s+")
        for i in xrange(0,num_tot_atoms):
            line = reader.readline()
            m3 = regexp.match(line)
            if m3 is None:
                reader.toPos(start_pos)
                return None
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

        reader.readline()
        
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
            
        return cls( num_atom_types, num_tot_atoms, atom_data_list, total_atom_data, spherical)
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
                atom_list.append( (m1.group(1), m1.group(2), (m1.group(3), m1.group(4), m1.group(5))))
                valid_data = True
                continue

            m2 = re.search("\s+(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m2 is not None:
                atom_list.append( (m2.group(1), "", (m2.group(2), m2.group(3), m2.group(4))))
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
            dipole = float(m1.group(1))
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
            dipole_x = float(m1.group(1))
            dipole_y = float(m2.group(1))
            dipole_z = float(m3.group(1))
        except ValueError:
            reader.toPos(start_pos)
            return None

        return cls([dipole_x, dipole_y, dipole_z])

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
            lumo_energy = float(m1.group(1))
            lumo_symmetry = int(m1.group(2))
            homo_energy = float(m2.group(1))
            homo_symmetry = int(m2.group(2))
            gap = float(m3.group(1))
        except ValueError:
            reader.toPos(start_pos)
            return None

        return cls(homo_energy, homo_symmetry, lumo_energy, lumo_symmetry, gap)

    # <<fold 

class BondLengthsToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self):
        return self._atom_list
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
                atom_list.append( ( (m5.group(1), m5.group(2)) , (m5.group(3), m5.group(4)) ,  m5.group(5)) )
                valid_data = True
                continue

            # symmetry label only on left atom
            m6 = re.search("bond distance:\s+(\w+)\s+(\d)\s+(\w+)\s+(\d+\.\d+)", line)
            if m6 is not None:
                atom_list.append( ( (m6.group(1), m6.group(2)) , (m6.group(3), "") ,  m6.group(4)) )
                valid_data = True
                continue

            # symmetry labels only on right atom
            m7 = re.search("bond distance:\s+(\w+)\s+(\w+)\s+(\d)\s+(\d+\.\d+)", line)
            if m7 is not None:
                atom_list.append( ( (m7.group(1), "") , (m7.group(2), m7.group(3)) ,  m7.group(4)) )
                valid_data = True
                continue

            # symmetry labels on no atoms
            m8 = re.search("bond distance:\s+(\w+)\s+(\w+)\s+(\d+\.\d+)", line)
            if m8 is not None:
                atom_list.append( ( (m8.group(1), "") , (m8.group(2), "") ,  m8.group(3)) )
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
            ] 
    return token_grammar


