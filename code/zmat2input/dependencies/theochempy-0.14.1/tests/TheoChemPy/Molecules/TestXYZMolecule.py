# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy import Units
from theochempy._theochempy import Measure
from theochempy._theochempy.Molecules import XYZMolecule
from theochempy._theochempy.Chemistry import PeriodicTable

import math

class TestXYZMolecule(unittest.TestCase):
    def testXYZMolecule(self): # fold>>
        mol = XYZMolecule.XYZMolecule( [
                                        (PeriodicTable.Carbon, Measure.Measure((1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Oxygen, Measure.Measure((-1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Nitrogen, Measure.Measure((-1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Fluorine, Measure.Measure((1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Hydrogen, Measure.Measure((0.0, 0.0, 1.0), Units.bohr)),
                                        ]
                                    )

        self.assertEqual(len(mol.elements()), 5)
        self.assertEqual(mol.elements()[0], PeriodicTable.Carbon)
        self.assertEqual(mol.elements()[1], PeriodicTable.Oxygen)
        self.assertEqual(mol.elements()[2], PeriodicTable.Nitrogen)
        self.assertEqual(mol.elements()[3], PeriodicTable.Fluorine)
        self.assertEqual(mol.elements()[4], PeriodicTable.Hydrogen)

        self.assertEqual(len(mol.atomPos()), 5)
        self.assertEqual(mol.atomPos()[0].__class__, Measure.Measure) 
        self.assertEqual(mol.atomPos()[1].__class__, Measure.Measure) 
        self.assertEqual(mol.atomPos()[2].__class__, Measure.Measure) 
        self.assertEqual(mol.atomPos()[3].__class__, Measure.Measure) 
        self.assertEqual(mol.atomPos()[4].__class__, Measure.Measure) 

        self.assertEqual(mol.atomPos()[0].value(), (1.0,1.0,0.0)  ) 
        self.assertEqual(mol.atomPos()[0].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[1].value(), (-1.0,1.0,0.0)  ) 
        self.assertEqual(mol.atomPos()[1].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[2].value(), (-1.0,-1.0,0.0)  ) 
        self.assertEqual(mol.atomPos()[2].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[3].value(), (1.0,-1.0,0.0)  ) 
        self.assertEqual(mol.atomPos()[3].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[4].value(), (0.0,0.0,1.0)  ) 
        self.assertEqual(mol.atomPos()[4].unit(), Units.bohr  ) 
        # <<fold

    def testTranslate(self): # fold>>
        mol = XYZMolecule.XYZMolecule( [
                                        (PeriodicTable.Carbon, Measure.Measure((1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Oxygen, Measure.Measure((-1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Nitrogen, Measure.Measure((-1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Fluorine, Measure.Measure((1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Hydrogen, Measure.Measure((0.0, 0.0, 1.0), Units.bohr)),
                                        ]
                                    )

        mol.translate( Measure.Measure((2.0,3.0,4.0),Units.bohr) )

        self.assertEqual(mol.atomPos()[0].value(), (3.0,4.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[0].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[1].value(), (1.0,4.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[1].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[2].value(), (1.0,2.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[2].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[3].value(), (3.0,2.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[3].unit(), Units.bohr  ) 
        self.assertEqual(mol.atomPos()[4].value(), (2.0,3.0,5.0)  ) 
        self.assertEqual(mol.atomPos()[4].unit(), Units.bohr  ) 

        mol = XYZMolecule.XYZMolecule( [
                                        (PeriodicTable.Carbon,Measure.Measure((1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Oxygen, Measure.Measure((-1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Nitrogen, Measure.Measure((-1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Fluorine, Measure.Measure((1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Hydrogen, Measure.Measure((0.0, 0.0, 1.0), Units.bohr)),
                                        ]
                                    )

        mol.translate( Measure.Measure( (2.0,3.0,4.0),Units.angstrom) )

        self.assertNotEqual(mol.atomPos()[0].value(), (3.0,4.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[0].unit(), Units.bohr  ) 
        self.assertNotEqual(mol.atomPos()[1].value(), (1.0,4.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[1].unit(), Units.bohr  ) 
        self.assertNotEqual(mol.atomPos()[2].value(), (1.0,-2.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[2].unit(), Units.bohr  ) 
        self.assertNotEqual(mol.atomPos()[3].value(), (3.0,-2.0,4.0)  ) 
        self.assertEqual(mol.atomPos()[3].unit(), Units.bohr  ) 
        self.assertNotEqual(mol.atomPos()[3].value(), (2.0,3.0,5.0)  ) 
        self.assertEqual(mol.atomPos()[3].unit(), Units.bohr  ) 
        # <<fold

    def testRotate(self): # fold>>
        mol = XYZMolecule.XYZMolecule( [
                                        (PeriodicTable.Carbon, Measure.Measure( (1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Oxygen, Measure.Measure( (-1.0, 1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Nitrogen, Measure.Measure( (-1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Fluorine, Measure.Measure( (1.0, -1.0, 0.0), Units.bohr)),
                                        (PeriodicTable.Hydrogen, Measure.Measure( (0.0, 0.0, 1.0), Units.bohr)),
                                        ]
                                    )

        mol.rotate( Measure.Measure( (0.0,0.0,1.0) ,Units.bohr), Measure.Measure(45.0, Units.degrees) )

        self.assertAlmostEqual(mol.atomPos()[0].value()[0], 0.0)
        self.assertAlmostEqual(mol.atomPos()[0].value()[1], math.sqrt(2.0))
        self.assertAlmostEqual(mol.atomPos()[0].value()[2], 0.0)
        self.assertEqual(mol.atomPos()[0].unit(), Units.bohr  ) 

        self.assertAlmostEqual(mol.atomPos()[1].value()[0], -math.sqrt(2.0))
        self.assertAlmostEqual(mol.atomPos()[1].value()[1], 0.0)
        self.assertAlmostEqual(mol.atomPos()[1].value()[2], 0.0)
        self.assertEqual(mol.atomPos()[1].unit(), Units.bohr  ) 

        self.assertAlmostEqual(mol.atomPos()[2].value()[0], 0.0)
        self.assertAlmostEqual(mol.atomPos()[2].value()[1], -math.sqrt(2.0))
        self.assertAlmostEqual(mol.atomPos()[2].value()[2], 0.0)
        self.assertEqual(mol.atomPos()[2].unit(), Units.bohr  ) 

        self.assertAlmostEqual(mol.atomPos()[3].value()[0], math.sqrt(2.0))
        self.assertAlmostEqual(mol.atomPos()[3].value()[1], 0.0)
        self.assertAlmostEqual(mol.atomPos()[3].value()[2], 0.0)
        self.assertEqual(mol.atomPos()[3].unit(), Units.bohr  ) 


        # <<fold
    def testCenterOfMass(self): # fold>>
        mol = XYZMolecule.XYZMolecule( [
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,0.0000000000,0.0000000000  ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,1.7920231678,-3.1038751750 ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,4.0095495535,2.3149145141  ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,6.3710924130,-3.1870231249 ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,8.5886187987,2.2317665642  ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,10.3806419665,-0.8721086108), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,1.7920231678,-1.0346250583 ), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,4.0095495535,0.2456643974  ), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,6.3710924130,-1.1177730082 ), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,8.5886187987,0.1625164475  ), Units.bohr) ),
                                        ]
                                    )

        center_of_mass = XYZMolecule.centerOfMass(mol)
        self.assertAlmostEqual(center_of_mass.value()[0], 0.000000, 6)
        self.assertAlmostEqual(center_of_mass.value()[1], 5.190321, 6)
        self.assertAlmostEqual(center_of_mass.value()[2], -0.436054, 6)
    # <<fold

    def testMomentsOfInertia(self): # fold>>
        mol = XYZMolecule.XYZMolecule( [
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,0.0000000000,0.0000000000  ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,1.7920231678,-3.1038751750 ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,4.0095495535,2.3149145141  ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,6.3710924130,-3.1870231249 ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,8.5886187987,2.2317665642  ), Units.bohr) ),
                                        (PeriodicTable.H, Measure.Measure( ( 0.0000000000,10.3806419665,-0.8721086108), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,1.7920231678,-1.0346250583 ), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,4.0095495535,0.2456643974  ), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,6.3710924130,-1.1177730082 ), Units.bohr) ),
                                        (PeriodicTable.C, Measure.Measure( ( 0.0000000000,8.5886187987,0.1625164475  ), Units.bohr) ),
                                        ]
                                    )

        inertia = XYZMolecule.momentsOfInertia(mol)
        self.assertEqual(len(inertia), 3)
        self.assertAlmostEqual(inertia[0][0].asUnit(Units.dalton * Units.angstrom * Units.angstrom).value(),  12.836878, 5)
        self.assertAlmostEqual(inertia[1][0].asUnit(Units.dalton * Units.angstrom * Units.angstrom).value(),  110.58507, 5)
        self.assertAlmostEqual(inertia[2][0].asUnit(Units.dalton * Units.angstrom * Units.angstrom).value(),  123.421950, 5)

        self.assertAlmostEqual(inertia[0][1].value()[0], 0.0) 
        self.assertAlmostEqual(inertia[0][1].value()[1], 0.994406, 5) 
        self.assertAlmostEqual(inertia[0][1].value()[2], 0.105628, 5) 

        self.assertAlmostEqual(inertia[1][1].value()[0], 0.0) 
        self.assertAlmostEqual(inertia[1][1].value()[1], -0.105628, 5) 
        self.assertAlmostEqual(inertia[1][1].value()[2], 0.994406, 5) 

        self.assertAlmostEqual(inertia[2][1].value()[0], 1.0) 
        self.assertAlmostEqual(inertia[2][1].value()[1], 0.0, 5) 
        self.assertAlmostEqual(inertia[2][1].value()[2], 0.0, 5) 
        #IA   12.836882          0.000000    0.994406    0.105628
        #IB  110.585080          0.000000   -0.105628    0.994406
        #IC  123.421963          1.000000    0.000000    0.000000
    # <<fold


if __name__ == '__main__':
    unittest.main()
    

