# @author Stefano Borini
from wavemoldb.ordfm import grrm2
from wavemoldb.ordfm.grrm2 import namespaces

import unittest
import rdflib
from rdflib import store
import os
def moduleDir():
    return os.path.dirname(__file__)

def getStore(rdf_file=None):
    _store = None
    
    s = rdflib.plugin.get('IOMemory', store.Store)('rdfstore')
    graph = rdflib.ConjunctiveGraph(s)
    if rdf_file is not None:
        graph.parse(os.path.join(moduleDir(),rdf_file))
    _store = s

    return _store
    
class TestAll(unittest.TestCase):
    def testInstantiation(self):
        graph = rdflib.ConjunctiveGraph(getStore())
        self.assertEqual( grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1").__class__, grrm2.EquilibriumStructure)
        self.assertEqual( grrm2.TransitionState.new(graph, "http://example.com/ts1").__class__, grrm2.TransitionState)
        self.assertEqual( grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1").__class__, grrm2.BarrierlessDissociated)
        self.assertEqual( grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1").__class__, grrm2.BarrierDissociated)
        self.assertEqual( grrm2.InterconversionStep.new(graph, "http://example.com/ic1").__class__, grrm2.InterconversionStep)
        self.assertEqual( grrm2.Interconversion.new(graph, "http://example.com/iconv1").__class__, grrm2.Interconversion)
        self.assertEqual( grrm2.RunData.new(graph, "http://example.com/rundata1").__class__, grrm2.RunData)
        self.assertEqual( grrm2.Run.new(graph, "http://example.com/run1").__class__, grrm2.Run)

        # technically these are abstract classes, they should not be instantiable, but owl does not allow abstract class definition
        self.assertEqual( grrm2.Molecule.new(graph, "http://example.com/mol1").__class__, grrm2.Molecule)
        self.assertEqual( grrm2.RunInput.new(graph, "http://example.com/runin1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunOutput.new(graph, "http://example.com/runout1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.InterconversionResult.new(graph, "http://example.com/icres1").__class__, grrm2.InterconversionResult)

    def testNoDoubleNew(self):
        graph = rdflib.ConjunctiveGraph(getStore())
        grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
        grrm2.TransitionState.new(graph, "http://example.com/ts1")
        grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
        grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
        grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
        grrm2.Interconversion.new(graph, "http://example.com/iconv1")
        grrm2.RunData.new(graph, "http://example.com/rundata1")
        grrm2.Run.new(graph, "http://example.com/run1")
        grrm2.Molecule.new(graph, "http://example.com/mol1")
        grrm2.RunInput.new(graph, "http://example.com/runin1")
        grrm2.RunOutput.new(graph, "http://example.com/runout1")
        grrm2.InterconversionResult.new(graph, "http://example.com/icres1")

        self.assertRaises( Exception, grrm2.EquilibriumStructure.new, graph, "http://example.com/eq1")
        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/ts1")
        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/blessdiss1")
        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/bdiss1")
        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/ic1")
        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/iconv1")
        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/rundata1")
        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/run1")
        self.assertRaises( Exception, grrm2.Molecule.new, graph, "http://example.com/mol1")
        self.assertRaises( Exception, grrm2.RunInput.new, graph, "http://example.com/runin1")
        self.assertRaises( Exception, grrm2.RunOutput.new, graph, "http://example.com/runout1")
        self.assertRaises( Exception, grrm2.InterconversionResult.new, graph, "http://example.com/icres1")

    def testGetNoReasoning(self):
        graph = rdflib.ConjunctiveGraph(getStore())
        grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
        grrm2.TransitionState.new(graph, "http://example.com/ts1")
        grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
        grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
        grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
        grrm2.Interconversion.new(graph, "http://example.com/iconv1")
        grrm2.RunData.new(graph, "http://example.com/rundata1")
        grrm2.Run.new(graph, "http://example.com/run1")
        grrm2.Molecule.new(graph, "http://example.com/mol1")
        grrm2.RunInput.new(graph, "http://example.com/runin1")
        grrm2.RunOutput.new(graph, "http://example.com/runout1")
        grrm2.InterconversionResult.new(graph, "http://example.com/icres1")

        self.assertEqual( grrm2.EquilibriumStructure.get(graph, "http://example.com/eq1").__class__, grrm2.EquilibriumStructure)
        self.assertEqual( grrm2.TransitionState.get(graph, "http://example.com/ts1").__class__, grrm2.TransitionState)
        self.assertEqual( grrm2.BarrierlessDissociated.get(graph, "http://example.com/blessdiss1").__class__, grrm2.BarrierlessDissociated)
        self.assertEqual( grrm2.BarrierDissociated.get(graph, "http://example.com/bdiss1").__class__, grrm2.BarrierDissociated)
        self.assertEqual( grrm2.InterconversionStep.get(graph, "http://example.com/ic1").__class__, grrm2.InterconversionStep)
        self.assertEqual( grrm2.Interconversion.get(graph, "http://example.com/iconv1").__class__, grrm2.Interconversion)
        self.assertEqual( grrm2.RunData.get(graph, "http://example.com/rundata1").__class__, grrm2.RunData)
        self.assertEqual( grrm2.Run.get(graph, "http://example.com/run1").__class__, grrm2.Run)
        self.assertEqual( grrm2.Molecule.get(graph, "http://example.com/mol1").__class__, grrm2.Molecule)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/runin1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/runout1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.InterconversionResult.get(graph, "http://example.com/icres1").__class__, grrm2.InterconversionResult)

    def testGetReasoning(self):
        graph = rdflib.ConjunctiveGraph(getStore())
        grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
        grrm2.TransitionState.new(graph, "http://example.com/ts1")
        grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
        grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
        grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
        grrm2.Interconversion.new(graph, "http://example.com/iconv1")
        grrm2.RunData.new(graph, "http://example.com/rundata1")
        grrm2.Run.new(graph, "http://example.com/run1")
        grrm2.Molecule.new(graph, "http://example.com/mol1")
        grrm2.RunInput.new(graph, "http://example.com/runin1")
        grrm2.RunOutput.new(graph, "http://example.com/runout1")
        grrm2.InterconversionResult.new(graph, "http://example.com/icres1")

        self.assertEqual( grrm2.InterconversionResult.get(graph, "http://example.com/eq1").__class__, grrm2.InterconversionResult)
        self.assertEqual( grrm2.InterconversionResult.get(graph, "http://example.com/ts1").__class__, grrm2.InterconversionResult)
        self.assertEqual( grrm2.InterconversionResult.get(graph, "http://example.com/blessdiss1").__class__, grrm2.InterconversionResult)
        self.assertEqual( grrm2.InterconversionResult.get(graph, "http://example.com/bdiss1").__class__, grrm2.InterconversionResult)

        self.assertEqual( grrm2.Molecule.get(graph, "http://example.com/eq1").__class__, grrm2.Molecule)
        self.assertEqual( grrm2.Molecule.get(graph, "http://example.com/ts1").__class__, grrm2.Molecule)
        self.assertEqual( grrm2.Molecule.get(graph, "http://example.com/blessdiss1").__class__, grrm2.Molecule)
        self.assertEqual( grrm2.Molecule.get(graph, "http://example.com/bdiss1").__class__, grrm2.Molecule)
        self.assertEqual( grrm2.Molecule.get(graph, "http://example.com/ic1").__class__, grrm2.Molecule)

        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/eq1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/ts1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/blessdiss1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/bdiss1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/ic1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/iconv1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/mol1").__class__, grrm2.RunOutput)
        self.assertEqual( grrm2.RunOutput.get(graph, "http://example.com/icres1").__class__, grrm2.RunOutput)

        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/eq1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/ts1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/blessdiss1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/bdiss1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/ic1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/mol1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/icres1").__class__, grrm2.RunInput)
        self.assertEqual( grrm2.RunInput.get(graph, "http://example.com/rundata1").__class__, grrm2.RunInput)

    def testDataProperty(self):
        graph = rdflib.ConjunctiveGraph(getStore())

        eq1 = grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
        ts1 = grrm2.TransitionState.new(graph, "http://example.com/ts1")
        blessdiss1 = grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
        bdiss1 = grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
        ic1 = grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
        iconv1 = grrm2.Interconversion.new(graph, "http://example.com/iconv1")
        rundata1 = grrm2.RunData.new(graph, "http://example.com/rundata1")
        run1 = grrm2.Run.new(graph, "http://example.com/run1")
        mol1 = grrm2.Molecule.new(graph, "http://example.com/mol1")
        runin1 = grrm2.RunInput.new(graph, "http://example.com/runin1")
        runout1 = grrm2.RunOutput.new(graph, "http://example.com/runout1")
        icres1 = grrm2.InterconversionResult.new(graph, "http://example.com/icres1")

        all_results = [eq1, ts1, blessdiss1, bdiss1, icres1]
        all_not_results = [iconv1, rundata1, run1, runin1, ic1, mol1, runout1]
        all_molecules = all_results + [ic1, mol1]
        all_not_molecules = [iconv1, rundata1, run1, runin1, runout1]
        all_runin = [runin1] + all_molecules
        all_runout = [runout1] + all_molecules

        for r in all_results:
            grrm2.zeroPointVibrationalEnergy(r).set(12.3)
            self.assertRaises( Exception, grrm2.zeroPointVibrationalEnergy(r).set, "hello")
        for r in all_not_results:
            self.assertRaises( Exception, grrm2.zeroPointVibrationalEnergy, r)

        for r in all_results:
            grrm2.structureNumber(r).set(1)
            self.assertRaises( Exception, grrm2.structureNumber(r).set, "hello")
        for r in all_not_results:
            self.assertRaises( Exception, grrm2.structureNumber, r)

        for r in [ic1]:
            grrm2.stepNumber(r).set(1)
            self.assertRaises( Exception, grrm2.stepNumber(r).set, "hello")
        for r in [eq1, ts1, blessdiss1, bdiss1, icres1, iconv1, rundata1, run1, runin1, mol1, runout1]:
            self.assertRaises( Exception, grrm2.stepNumber, r)

        for r in all_molecules:
            grrm2.spinMultiplicity(r).set(1)
            self.assertRaises( Exception, grrm2.spinMultiplicity(r).set, "hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.spinMultiplicity, r)

        for r in all_molecules:
            grrm2.spin(r).set(1.4)
            self.assertRaises( Exception, grrm2.spin(r).set, "hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.spin, r)

        for r in all_molecules:
            grrm2.smiles(r).set("hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.smiles, r)

        for r in all_molecules:
            grrm2.normalModesEigenvalues(r).set([1,2,3])
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.normalModesEigenvalues, r)

        for r in [rundata1]:
            grrm2.method(r).set("hello")
        for r in [ eq1, ts1, blessdiss1, bdiss1 , ic1 , iconv1, run1, mol1 , runin1, runout1, icres1 ]:
            self.assertRaises( Exception, grrm2.method, r)

        for r in all_molecules:
            grrm2.mass(r).set(1.4)
            self.assertRaises( Exception, grrm2.mass(r).set, "hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.mass, r)

        for r in [rundata1]:
            grrm2.job(r).set("hello")
        for r in [ eq1, ts1, blessdiss1, bdiss1 , ic1 , iconv1, run1, mol1 , runin1, runout1, icres1 ]:
            self.assertRaises( Exception, grrm2.job, r)

        for r in all_molecules:
            grrm2.inchi(r).set("hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.inchi, r)

        for r in all_molecules:
            grrm2.hillFormula(r).set("hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.hillFormula, r)

        for r in all_molecules:
            grrm2.geometry(r).set({})
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.geometry, r)

        for r in all_molecules:
            grrm2.energy(r).set(1.4)
            self.assertRaises( Exception, grrm2.energy(r).set, "hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.energy, r)

        for r in all_molecules:
            grrm2.charge(r).set(1.4)
            self.assertRaises( Exception, grrm2.charge(r).set, "hello")
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.charge, r)
       
        for r in all_molecules:
            grrm2.canostSerial(r).set(["foo"])
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.canostSerial, r)

        for r in all_molecules:
            grrm2.canostPlanar(r).set(["foo"])
        for r in all_not_molecules:
            self.assertRaises( Exception, grrm2.canostPlanar, r)

        for r in [rundata1]:
            grrm2.basisSet(r).set("hello")
        for r in [ eq1, ts1, blessdiss1, bdiss1 , ic1 , iconv1, run1, mol1 , runin1, runout1, icres1 ]:
            self.assertRaises( Exception, grrm2.basisSet, r)

    def testObjectProperty(self):
        graph = rdflib.ConjunctiveGraph(getStore())

        eq1 = grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
        ts1 = grrm2.TransitionState.new(graph, "http://example.com/ts1")
        blessdiss1 = grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
        bdiss1 = grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
        ic1 = grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
        iconv1 = grrm2.Interconversion.new(graph, "http://example.com/iconv1")
        rundata1 = grrm2.RunData.new(graph, "http://example.com/rundata1")
        run1 = grrm2.Run.new(graph, "http://example.com/run1")
        mol1 = grrm2.Molecule.new(graph, "http://example.com/mol1")
        runin1 = grrm2.RunInput.new(graph, "http://example.com/runin1")
        runout1 = grrm2.RunOutput.new(graph, "http://example.com/runout1")
        icres1 = grrm2.InterconversionResult.new(graph, "http://example.com/icres1")

        grrm2.runInput(run1).add(eq1)
        grrm2.runInput(run1).add(ts1)
        grrm2.runInput(run1).add(ic1)
        grrm2.runInput(run1).add(blessdiss1)
        grrm2.runInput(run1).add(bdiss1)
        grrm2.runInput(run1).add(icres1)
        grrm2.runInput(run1).add(mol1)
        grrm2.runInput(run1).add(runin1)
        grrm2.runInput(run1).add(rundata1)

        self.assertRaises(Exception, grrm2.runInput(run1).add, iconv1 )
        self.assertRaises(Exception, grrm2.runInput(run1).add, runout1 )
        self.assertRaises(Exception, grrm2.runInput(run1).add, run1 )

        grrm2.runOutput(run1).add(eq1)
        grrm2.runOutput(run1).add(ts1)
        grrm2.runOutput(run1).add(ic1)
        grrm2.runOutput(run1).add(blessdiss1)
        grrm2.runOutput(run1).add(bdiss1)
        grrm2.runOutput(run1).add(iconv1)
        grrm2.runOutput(run1).add(icres1)
        grrm2.runOutput(run1).add(mol1)
        grrm2.runOutput(run1).add(runout1)

        self.assertRaises(Exception, grrm2.runOutput(run1).add, runin1 )
        self.assertRaises(Exception, grrm2.runOutput(run1).add, rundata1 )
        self.assertRaises(Exception, grrm2.runOutput(run1).add, run1 )

        grrm2.interconversionStart(iconv1).set(eq1)
        grrm2.interconversionEnd(iconv1).set(ts1)

        self.assertRaises(Exception, grrm2.interconversionStart(iconv1).set, run1)
        self.assertRaises(Exception, grrm2.interconversionEnd(iconv1).set, run1)

    def testAll(self):
        graph = rdflib.ConjunctiveGraph(getStore())

        eq1 = grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
        ts1 = grrm2.TransitionState.new(graph, "http://example.com/ts1")
        blessdiss1 = grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
        bdiss1 = grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
        ic1 = grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
        iconv1 = grrm2.Interconversion.new(graph, "http://example.com/iconv1")
        rundata1 = grrm2.RunData.new(graph, "http://example.com/rundata1")
        run1 = grrm2.Run.new(graph, "http://example.com/run1")
        mol1 = grrm2.Molecule.new(graph, "http://example.com/mol1")
        runin1 = grrm2.RunInput.new(graph, "http://example.com/runin1")
        runout1 = grrm2.RunOutput.new(graph, "http://example.com/runout1")
        icres1 = grrm2.InterconversionResult.new(graph, "http://example.com/icres1")

        self.assertEqual(len(list(grrm2.Molecule.all(graph))), 7)
        self.assertEqual(len(list(grrm2.InterconversionStep.all(graph))), 1)

    def testNoDisjointClassesNew(self):
        pass
#        graph = rdflib.ConjunctiveGraph(getStore())
#        grrm2.EquilibriumStructure.new(graph, "http://example.com/eq1")
#        grrm2.TransitionState.new(graph, "http://example.com/ts1")
#        grrm2.BarrierlessDissociated.new(graph, "http://example.com/blessdiss1")
#        grrm2.BarrierDissociated.new(graph, "http://example.com/bdiss1")
#        grrm2.InterconversionStep.new(graph, "http://example.com/ic1")
#        grrm2.Interconversion.new(graph, "http://example.com/iconv1")
#        grrm2.RunData.new(graph, "http://example.com/rundata1")
#        grrm2.Run.new(graph, "http://example.com/run1")
#        grrm2.Molecule.new(graph, "http://example.com/mol1")
#        grrm2.RunInput.new(graph, "http://example.com/runin1")
#        grrm2.RunOutput.new(graph, "http://example.com/runout1")
#        grrm2.InterconversionResult.new(graph, "http://example.com/icres1")
#
#        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/eq1")
#        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/eq1")
#        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/eq1")
#        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/eq1")
#        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/eq1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/eq1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/eq1")
#
#        self.assertRaises( Exception, grrm2.EquilibriumStructure.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/ts1")
#
#        self.assertRaises( Exception, grrm2.EquilibriumStructure.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/blessdiss1")
#
#        self.assertRaises( Exception, grrm2.EquilibriumStructure.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/bdiss1")
#
#        self.assertRaises( Exception, grrm2.EquilibriumStructure.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/ic1")
#
#        self.assertRaises( Exception, grrm2.EquilibriumStructure.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/iconv1")

#        self.assertRaises( Exception, grrm2.TransitionState.new, graph, "http://example.com/ts1")
#        self.assertRaises( Exception, grrm2.BarrierlessDissociated.new, graph, "http://example.com/blessdiss1")
#        self.assertRaises( Exception, grrm2.BarrierDissociated.new, graph, "http://example.com/bdiss1")
#        self.assertRaises( Exception, grrm2.InterconversionStep.new, graph, "http://example.com/ic1")
#        self.assertRaises( Exception, grrm2.Interconversion.new, graph, "http://example.com/iconv1")
#        self.assertRaises( Exception, grrm2.RunData.new, graph, "http://example.com/rundata1")
#        self.assertRaises( Exception, grrm2.Run.new, graph, "http://example.com/run1")
#        self.assertRaises( Exception, grrm2.Molecule.new, graph, "http://example.com/mol1")
#        self.assertRaises( Exception, grrm2.RunInput.new, graph, "http://example.com/runin1")
#        self.assertRaises( Exception, grrm2.RunOutput.new, graph, "http://example.com/runout1")
#        self.assertRaises( Exception, grrm2.InterconversionResult.new, graph, "http://example.com/icres1")

    def notestExistence(self):
        eq2 = grrm2.EquilibriumStructure.get(graph, "http://example.com/eq1")
        self.assertEqual(eq2.__class__, grrm2.EquilibriumStructure)
        self.assertEqual(eq.uri(), eq2.uri())


    def notestDisjointClasses(self):
        # disjoint classes
        self.assertRaises(Exception, grrm2.TransitionState.get, graph, "http://example.com/eq1")

        self.assertEqual(grrm2.InterconversionResult.get(graph, "http://example.com/eq1").__class__, grrm2.InterconversionResult)



if __name__ == '__main__':
    unittest.main()
    
