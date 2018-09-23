"""This module provides access to python-quantities (pyquantities) units, plus
additional units we define"""

from quantities import *
import quantities as _quantities

bohr = 1.0 * _quantities.constants.Bohr_radius
dalton = 1.0 * _quantities.units.atomic_mass_unit
debye = 1.0e-18 * _quantities.units.statcoulomb * _quantities.units.cm
atomic_unit_of_1st_hyperpolarizability = 1.0 * _quantities.constants.atomic_unit_of_1st_hyperpolarizablity # typo is ok!
atomic_unit_of_2nd_hyperpolarizability = 1.0 * _quantities.constants.atomic_unit_of_2nd_hyperpolarizablity # typo is ok!

atomic_unit_of_electric_polarizability = 1.0 * _quantities.constants.atomic_unit_of_electric_polarizablity # typo is ok!

hbar = 1.0 * _quantities.constants.hbar

kbyte = 1000 * _quantities.units.byte 
kB = kbyte
Mbyte = 1000 * 1000 * _quantities.units.byte 
MB = Mbyte
Gbyte = 1000 * 1000 * 1000 * _quantities.units.byte 
GB = Gbyte
Tbyte = 1000 * 1000 * 1000 * 1000 * _quantities.units.byte
TB = Tbyte

kibibyte = 1024 * _quantities.units.byte
KiB = kibibyte
mebibyte = 1024 * 1024 * _quantities.units.byte
MiB = mebibyte
gibibyte = 1024 * 1024 * 1024 * _quantities.units.byte
GiB = gibibyte
tebibyte = 1024 * 1024 * 1024 * 1024 * _quantities.units.byte
TiB = tebibyte

class UnitUnknown(_quantities.unitquantity.IrreducibleUnit): pass

unknown = UnitUnknown("unknown")
