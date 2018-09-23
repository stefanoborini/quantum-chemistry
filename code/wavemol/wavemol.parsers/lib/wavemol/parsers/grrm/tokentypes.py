from wavemol.core import units
import re

class HeaderDissociatedToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        regexp = re.compile("List of Dissociated Structures")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        return None 
        # <<fold

class HeaderEquilibriumToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        regexp = re.compile("List of Equilibrium Structures")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        return None 
        # <<fold

class HeaderTransitionToken:
    def __init__(self): # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        regexp = re.compile("List of Transition Structures")
        line = reader.readline()
        if regexp.search(line):
            return cls()

        return None 
        # <<fold

class StructureHeaderToken:
    def __init__(self, type, number, symmetry): #  fold>>
        self._type = type
        self._number = number
        self._symmetry = symmetry
    # <<fold
    def type(self): # fold>>
        return self._type
    # <<fold
    def number(self): # fold>>
        return self._number
    # <<fold
    def symmetry(self): # fold>>
        return self._symmetry
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens):  # fold>>
        line = reader.readline()
        
        m = re.search("# Geometry of (\S+) (\d+), SYMMETRY = (\S+)", line)

        if m is None:
            return None
        return cls( type=m.group(1), number=int(m.group(2)), symmetry=m.group(3))
class GeometryToken:
    def __init__(self, atom_list): # fold>>
        self._atom_list = atom_list
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>

        atom_list = []

        valid_data = False
        for line in reader:
     
            m1 = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m1 is not None:
                atom_label = m1.group(1)
                position = [ float(m1.group(2)), float(m1.group(3)), float(m1.group(4))] * units.angstrom
                atom_list.append( (atom_label, position) )
                valid_data = True
                continue

            break
       
        reader.readbackline()
        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            return None

        return cls(atom_list)

    # <<fold 


class EnergyToken:
    def __init__(self, energy): #  fold>>
        self._energy = energy
        # <<fold
    def energy(self): # fold>>
        return self._energy
        # <<fold 
    @classmethod
    def match(cls, reader, previous_tokens):  # fold>>
        line = reader.readline()
        m = re.search("Energy\s+=\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( float(m.group(1)) * units.hartree )

        return None
    # <<fold


class SpinToken:
    def __init__(self, spin): #  fold>>
        self._spin = spin
        # <<fold
    def spin(self): # fold>>
        return self._spin
        # <<fold 
    @classmethod
    def match(cls, reader, previous_tokens):  # fold>>
        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+=\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( float(m.group(1)) * units.hbar )

        return None
    # <<fold

class ZPVEToken:
    def __init__(self, zpve): #  fold>>
        self._zpve = zpve
        # <<fold
    def zpve(self): # fold>>
        return self._zpve
        # <<fold 
    @classmethod
    def match(cls, reader, previous_tokens):  # fold>>
        line = reader.readline()
        m = re.search("ZPVE\s+=\s+(-?\d*\.\d*)", line)
        if m is not None:
            return cls( float(m.group(1)) * units.hartree )

        return None
    # <<fold


class NormalModesToken:
    def __init__(self, eigenvalues): # fold>>
        self._eigenvalues = eigenvalues
    def eigenvalues(self):
        return self._eigenvalues
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        line = reader.readline()
        eigenvalues = []
        
        m = re.search("Normal mode eigenvalues : nmode = (\d+)", line)
        if m is None:
            return None

        num_of_eigenvalues = int(m.group(1))

        num_of_full_lines = int(num_of_eigenvalues / 5)
        remainder = num_of_eigenvalues % 5


        for i in xrange(num_of_full_lines):
            line = reader.readline()
            m1 = re.search("(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)", line)
            if m1 is None:
                return None
            for j in xrange(1,6):
                eigenvalues.append(float(m1.group(j)) * units.hartree )

        if remainder != 0:
            line = reader.readline()
            m2 = re.search("\s+".join(["(-?\d*\.\d*)"]*remainder), line)
            if m2 is None:
                return None
            for j in xrange(1,remainder+1):
                eigenvalues.append(float(m2.group(j))*units.hartree)
    
        return cls(eigenvalues)
        # <<fold 
# <<fold            

class ConnectionToken:
    def __init__(self, first, second): #  fold>>
        self._first = first
        self._second = second
        # <<fold
    def first(self): # fold>>
        return self._first
        # <<fold 
    def second(self): # fold>>
        return self._second
        # <<fold 
    @classmethod
    def match(cls, reader, previous_tokens):  # fold>>
        line = reader.readline()
        m = re.search("CONNECTION : (\S+) - (\S+)", line)
        if m is not None:
            return cls( m.group(1), m.group(2))

        return None
    # <<fold


# Input tokens

class CommandDirectiveToken:
    def __init__(self, command_line, job_string, method_string, basis_set_string) : # fold>>
        self._command_line = command_line
        self._job_string = job_string
        self._method_string = method_string
        self._basis_set_string = basis_set_string
    # <<fold
    def commandLine(self):
        return self._command_line
    def jobString(self):
        return self._job_string
    def methodString(self):
        return self._method_string
    def basisSetString(self):
        return self._basis_set_string
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        regexp = re.compile("^#\s+(.*)$")
        line = reader.readline()
        m1 = regexp.search(line)
        if m1 is not None:
            command_line = m1.group(1)
            parts = command_line.split("/") 
            if len(parts) != 3:
                return None

            return cls(command_line, parts[0], parts[1], parts[2])

        return None 
class InputGeometryToken:
    def __init__(self, atom_list, charge, spin_multiplicity): # fold>>
        self._atom_list = atom_list
        self._charge = charge
        self._spin_multiplicity = spin_multiplicity
    # <<fold 
    def atomList(self): # fold>>
        return self._atom_list
    # <<fold
    def charge(self): # fold>>
        return self._charge
    # <<fold
    def spinMultiplicity(self): # fold>>
        return self._spin_multiplicity
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        atom_list = []

        valid_data = False
        for line in reader:
            m0 = re.search("^(\d)\s+(\d)\s*$", line)
            if m0 is not None:
                charge = int(m0.group(1))
                spin_multiplicity = int(m0.group(2))
                continue

            m1 = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m1 is not None:
                atom_label = m1.group(1)
                position = [float(m1.group(2)), float(m1.group(3)), float(m1.group(4))] * units.angstrom
                atom_list.append( (atom_label, position) )
                valid_data = True
                continue

            break
       
        reader.readbackline()
        if len(atom_list) == 0:
            valid_data = False

        if valid_data == False:
            return None

        return cls(atom_list, charge, spin_multiplicity)
class OptionsHeaderToken:
    def __init__(self) : # fold>>
        pass
    # <<fold
    @classmethod
    def match(cls, reader, previous_tokens): # fold>> 
        line = reader.readline()
        if line.strip().lower() == "options":
            return cls()

        return None 
class NRunOptionToken:
    def __init__(self, value): #  fold>>
        self._value = value
        # <<fold
    def value(self): # fold>>
        return self._value
        # <<fold 
    @classmethod
    def match(cls, reader, previous_tokens):  # fold>>
        line = reader.readline()
        m = re.search("(\w*?)\s+=\s+(\d+)", line)
        if m is not None:
            if m.group(1).strip().lower() == "nrun":
                return cls(int(m.group(2)))

        return None

# TS analysis tokens

class OptimizationHeaderToken:
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("OPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTOPTO", line)
        if m is None:
            return None
        return cls()
class OptimizationIterationToken:
    def __init__(self, iteration_number, atom_list, energy, spin, lambda_, trust_radius, step_radius, max_force, rms_force, max_displacement, rms_displacement ): 
        self._iteration_number = iteration_number
        self._atom_list = atom_list
        self._energy = energy
        self._spin = spin
        self._lambda_ = lambda_
        self._trust_radius = trust_radius
        self._step_radius = step_radius
        self._max_force = max_force
        self._rms_force = rms_force
        self._max_displacement = max_displacement
        self._rms_displacement = rms_displacement
    def iteration_number(self):
        return self._iteration_number
    def atomList(self):
        return self._atom_list 
    def energy(self):
        return self._energy
    def spin(self):
        return self._spin
    def lambda_(self):
        return self._lambda_
    def trust_radius(self):
        return self._trust_radius 
    def stepRadius(self):
        return self._step_radius
    def maxForce(self):
        return self._max_force
    def rmsForce(self):
        return self._rms_force
    def maxDisplacement(self):
        return self._max_displacement
    def rmsDisplacement(self):
        return self._rms_displacement 
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
                
        m = re.search("# ITR. (\d+)", line)
        if m is None:
            return None

        iteration_number = int(m.group(1))

        atom_list = []
        for line in reader:
            m = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            atom_symbol = m.group(1)
            position = [float(m.group(2)), float(m.group(3)), float(m.group(4))] * units.angstrom
            atom_list.append( (atom_symbol, position) )

        m = re.search("Item\s+Value\s+Threshold", line)
        if m is None:
            return None

        line = reader.readline()
        m = re.search("ENERGY\s+(-?\d+\.\d+)", line)
        if m is None:
            return None

        energy = float(m.group(1)) * units.hartree

        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        
        spin = float(m.group(1)) * units.hbar

        line = reader.readline()
        m = re.search("LAMDA\s+(-?\d+\.\d+)", line) # typo ok
        if m is None:
            return None
        lambda_ = float(m.group(1)) * units.unknown

        line = reader.readline()
        m = re.search("TRUST RADII\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        trust_radius = float(m.group(1)) * units.unknown
        
        line = reader.readline()
        m = re.search("STEP RADII\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        step_radius = float(m.group(1)) * units.unknown

        line = reader.readline()
        m = re.search("Maximum\s+Force\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        max_force = [ float(m.group(1)) * units.unknown, float(m.group(1))* units.unknown ]

        line = reader.readline()
        m = re.search("RMS\s+Force\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        rms_force = [ float(m.group(1)) * units.unknown, float(m.group(1))* units.unknown ]

        line = reader.readline()
        m = re.search("Maximum\s+Displacement\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        max_displacement = [ float(m.group(1)) * units.unknown, float(m.group(1))* units.unknown ]

        line = reader.readline()
        m = re.search("RMS\s+Displacement\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        rms_displacement = [ float(m.group(1)) * units.unknown, float(m.group(1))* units.unknown ]

        return cls(iteration_number, atom_list, energy, spin, lambda_, trust_radius, step_radius, max_force, rms_force, max_displacement, rms_displacement)
class OptimizationFinalStructureToken:
    def __init__(self, symmetry, atom_list, energy, spin, zpve): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
                
        m = re.search("Optimized structure, SYMMETRY = (\w+)", line)
        if m is None:
            return None

        symmetry = m.group(1)

        atom_list = []
        for line in reader:
            m = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            atom_symbol = m.group(1)
            position = [float(m.group(2)), float(m.group(3)), float(m.group(4))] * units.angstrom
            atom_list.append( (atom_symbol, position) )

        m = re.search("ENERGY\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None

        energy = float(m.group(1)) * units.hartree

        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        
        spin = float(m.group(1)) * units.hbar

        line = reader.readline()
        m = re.search("ZPVE\s+=\s+(-?\d*\.\d*)", line)
        if m is None:
            return None

        zpve =  float(m.group(1)) * units.hartree

        return cls( symmetry, atom_list, energy, spin, zpve )
class NormalModesTSToken:
    def __init__(self, eigenvalues): # fold>>
        self._eigenvalues = eigenvalues
    def eigenvalues(self):
        return self._eigenvalues
    @classmethod
    def match(cls, reader, previous_tokens): # fold>>
        line = reader.readline()
        eigenvalues = []
        
        m = re.search("NORMAL MODE EIGENVALUE : N_MODE = (\d+)", line)
        if m is None:
            return None

        num_of_eigenvalues = int(m.group(1))

        num_of_full_lines = int(num_of_eigenvalues / 5)
        remainder = num_of_eigenvalues % 5


        for i in xrange(num_of_full_lines):
            line = reader.readline()
            m1 = re.search("(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)\s+(-?\d*\.\d*)", line)
            if m1 is None:
                return None
            for j in xrange(1,6):
                eigenvalues.append(float(m1.group(j)) * units.hartree )

        if remainder != 0:
            line = reader.readline()
            m2 = re.search("\s+".join(["(-?\d*\.\d*)"]*remainder), line)
            if m2 is None:
                return None
            for j in xrange(1,remainder+1):
                eigenvalues.append(float(m2.group(j))*units.hartree)

        return cls(eigenvalues)
class MinimumPointFoundHeaderToken:
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("Minimum point was found", line)
        if m is None:
            return None
        return cls()
class InitialStructureToken:
    def __init__(self, atom_list, energy, spin): 
        self._atom_list = atom_list
        self._energy = energy
        self._spin = spin
    def atomList(self):
        return self._atom_list
    def energy(self):
        return self._energy
    def spin(self):
        return self._spin

    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
                
        m = re.search("INITIAL STRUCTURE", line)
        if m is None:
            return None

        atom_list = []
        for line in reader:
            m = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            atom_symbol = m.group(1)
            position = [float(m.group(2)), float(m.group(3)), float(m.group(4))] * units.angstrom
            atom_list.append( (atom_symbol, position) )

        m = re.search("ENERGY\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None

        energy = float(m.group(1)) * units.hartree

        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        
        spin = float(m.group(1)) * units.hbar

        return cls( atom_list, energy, spin )
class IRCHeaderToken:
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("IRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCIRCI", line)
        if m is None:
            return None
        return cls()
class EnergyProfileToken:
    def __init__(self, energy_profile_direct, energy_profile_reverse): 
        pass
    def energyProfileDirect(self):
        self._energy_profile_direct
    def energyProfileReverse(self):
        self._energy_profile_reverse
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()

        m = re.search("Energy profile along IRC", line)
        if m is None:
            return None

        line = reader.readline()
        m = re.search("Length\s+\(A\s+amu1/2\)\s+Energy\s+\(Hartree\)", line)
        if m is None:
            return None

        energy_profile_direct = []
        for line in reader:
            m = re.search("(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            entry = ( float(m.group(1)) * units.angstrom * units.dalton**0.5 , float(m.group(2))*units.hartree )
            energy_profile_direct.append(entry) 

        m = re.search("Reverse", line)
        if m is None:
            return None

        line = reader.readline()
        m = re.search("Length\s+\(A\s+amu1/2\)\s+Energy\s+\(Hartree\)", line)
        if m is None:
            return None
        
        energy_profile_reverse = []
        for line in reader:
            m = re.search("(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            entry = ( float(m.group(1)) * units.angstrom * units.dalton**0.5 , float(m.group(2))*units.hartree )
            energy_profile_reverse.append(entry) 

        return cls(energy_profile_direct, energy_profile_reverse)
class BackwardIRCHeaderToken: 
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("IRC FOLLOWING ALONG BACKWARD DIRECTION", line)
        if m is None:
            return None
        return cls()
class ForwardIRCHeaderToken:
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("IRC FOLLOWING \(FORWARD\) STARTING FROM FIRST-ORDER SADDLE", line)
        if m is None:
            return None
        return cls()
class IRCFollowingResultsToken: 
    def __init__(self, forward, backward): 
        self._forward = forward
        self._backward = backward
    def forward(self):
        return self._forward
    def backward(self):
        return self._backward

    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        m = re.search("Results of IRC following", line)
        if m is None:
            return None
       
        line = reader.readline()
        m = re.search("FORWARD\s+:\s+Reached\s+(\w+)\s+(\d+)", line)
        if m is None:
            return None
        forward = ( m.group(1), int(m.group(2)))

        line = reader.readline()
        m = re.search("BACKWARD\s+:\s+Reached\s+(\w+)\s+(\d+)", line)
        if m is None:
            return None
        backward = ( m.group(1), int(m.group(2)))

        return cls(forward, backward)
class IRCStepToken:
    def __init__(self, step, atom_list, energy, spin): 
        self._step= step
        self._atom_list = atom_list
        self._energy = energy
        self._spin = spin
    def step(self):
        return self._step
    def atomList(self):
        return self._atom_list 
    def energy(self):
        return self._energy
    def spin(self):
        return self._spin
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
                
        m = re.search("# STEP (\d+)", line)
        if m is None:
            return None

        step_number = int(m.group(1))

        atom_list = []
        for line in reader:
            m = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            atom_symbol = m.group(1)
            position = [float(m.group(2)), float(m.group(3)), float(m.group(4))] * units.angstrom
            atom_list.append( (atom_symbol, position) )

        m = re.search("ENERGY\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None

        energy = float(m.group(1)) * units.hartree

        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        
        spin = float(m.group(1)) * units.hbar

        return cls(step_number, atom_list, energy, spin)
class DCReachedToken: 
    def __init__(self, atom_list, energy, spin, zpve): 
        self._atom_list = atom_list
        self._energy = energy
        self._spin = spin
        self._zpve = zpve
    def atomList(self):
        return self._atom_list 
    def energy(self):
        return self._energy
    def spin(self):
        return self._spin
    def zpve(self):
        return self._zpve
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
                
        m = re.search("MAXIMUM INTER-PARTICLE DISTANCE EXCEEDED, REACHED DC", line)
        if m is None:
            return None

        atom_list = []
        for line in reader:
            m = re.search("(\w+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", line)
            if m is None:
                break
            atom_symbol = m.group(1)
            position = [float(m.group(2)), float(m.group(3)), float(m.group(4))] * units.angstrom
            atom_list.append( (atom_symbol, position) )

        m = re.search("ENERGY\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None

        energy = float(m.group(1)) * units.hartree

        line = reader.readline()
        m = re.search("Spin\(\*\*2\)\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        
        spin = float(m.group(1)) * units.hbar

        line = reader.readline()
        m = re.search("ZPVE\s+=\s+(-?\d+\.\d+)", line)
        if m is None:
            return None
        
        zpve = float(m.group(1)) * units.hartree

        return cls(atom_list, energy, spin, zpve)
class EQWithinStepsizeHeaderToken:
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("EQ EXIST WITHIN STEPSIZE, OPTIMIZATION CARRIED OUT", line)
        if m is None:
            return None
        return cls()
class GradientVectorToken:
    def __init__(self, vector):
        self._vector = vector
    def vector(self):
        return self._vector
    @classmethod
    def match(cls, reader, previous_tokens):
        
        line = reader.readline()
        
        m = re.search("GRADIENT VECTOR", line)
        if m is None:
            return None

        gradient_vector = []
        for line in reader:
            m = re.search("(-?\d+\.\d+)", line)
            if m is None:
                break
            gradient_vector.append( float(m.group(1)) )
        
        gradient_vector = gradient_vector * units.unknown
        
        return cls(gradient_vector)

class DissociationFragmentsToken:
    def __init__(self, fragments):
        self._fragments = fragments
    def numFragments(self):
        return len(self._fragments)
    def fragment(self, index):
        return self._fragments[index]
    def fragments(self):
        return self._fragments
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("Dissociation fragments : nfrag = (\d+)", line)
        if m is None:
            return None

        num_fragments = int(m.group(1))

        reader.readline() # trash one

        fragments = [] 
        for i in xrange(num_fragments):
            line = reader.readline()
            m = re.search("DF\s+"+str(i)+"\s+=\s+\{(.*)\}", line)
            if m is None:
                break
            fragment = [int(x.strip()) for x in m.group(1).split(",")]
            fragments.append(fragment)

        return cls(fragments)

# upper dc (UDC, previously dc) analysis token

class SteepestDescentHeaderToken:
    def __init__(self): 
        pass
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        
        m = re.search("STEEPEST-DESCENT PATH FOLLOWING STARTING FROM NON-STATIONARY POINT", line)
        if m is None:
            return None
        return cls()

class DownhillWalkingResultToken: 
    def __init__(self, result): 
        self._result = result
    def result(self):
        return self._result
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        m = re.search("Result of downhill walking : Reached\s+(\w+)\s+(\d+)", line)
        if m is None:
            return None
        result = ( m.group(1), int(m.group(2)))

        return cls(result)
