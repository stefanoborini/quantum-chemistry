from unum import Unum
from unum.units import M as __M
from unum.units import J as __J
from unum.units import ANGSTROM as __ANGSTROM
from unum.units import ARCDEG as __ARCDEG
from unum.units import RAD as __RAD
from unum.units import U as __U
from unum.units import EV as __EV
from unum.units import C as __C

meter = __M

bohr = Unum.unit('bohr' , 5.2917720859e-11 * meter)
angstrom = __ANGSTROM
Ang = angstrom

degrees = __ARCDEG
deg = degrees
radians = __RAD
rad = radians

# space occupation
byte = Unum.unit("byte")
kbyte = Unum.unit("kilobyte", 1000 * byte)
Mbyte = Unum.unit("megabyte", 1000000 * byte)
Gbyte = Unum.unit("gigabyte", 1000000000 * byte)

kibyte = Unum.unit("kibibyte", 1024 * byte)
Mibyte = Unum.unit("mebibyte", 1024 * 1024 * byte)
Gibyte = Unum.unit("gibibyte", 1024 * 1024 * 1024 * byte)

dalton = Unum.unit("dalton", 1.0*__U)
Da = dalton
coulomb = Unum.unit("coulomb", 1.0*__C)
# energies
joule = Unum.unit("joule", 1.0 * __J)
hartree = Unum.unit("hartree", 4.35974381e-18 * joule)

electronvolt = __EV
eV = electronvolt
debye = Unum.unit("debye", 3.335640952e-30 * coulomb * meter)

statcoulomb = Unum.unit("statcoulomb")
statC=statcoulomb
esu = statcoulomb

alpha_au = Unum.unit("polarizability atomic units")
beta_au = Unum.unit("1st hyperpolarizability atomic units")
gamma_au = Unum.unit("2nd hyperpolarizability atomic units")
frequency_au = Unum.unit("frequency atomic units")

unknown = Unum.unit("unknown")

