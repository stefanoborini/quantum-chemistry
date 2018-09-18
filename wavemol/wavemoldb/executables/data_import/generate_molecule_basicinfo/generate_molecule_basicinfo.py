#!/usr/bin/env python
import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
from lib import uuid
from wavemoldb import ordfm
from wavemoldb.ordfm import grrm2
from wavemoldb.ordfm import contexts
import rdflib
from application import graphstore
from rdflib.Graph import Graph
import getopt
import helperfuncs

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ['DJANGO_SETTINGS_MODULE'] = "settings"

class Options:
    def __init__(self, argv): 
        self.submission_uuid = None
        self._getOptions(argv)

    def _getOptions(self,argv):
        opts, args=getopt.getopt(argv[1:], "i:vh", ["id=","help"])

        for opt in opts:
            if opt[0] in ["-i", "--id"]:
                self.submission_uuid = str(uuid.UUID(opt[1]))
            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)

def _usage(error=None): 
    print "Usage : "+os.path.basename(sys.argv[0])+" --id=submission_uuid"
    print ""
    print "Generate xyz for all molecules in a given submission"
    print ""
    if error is not None:
        print ""
        print error
        print ""

def main():
    options=Options(sys.argv)

    system_uuid = helperfuncs.getSystemUuid(graphstore.store(),  options.submission_uuid)
    submission_info_subgraph = Graph(graphstore.store(), identifier=contexts.CONTEXT_NS.SubmissionInfo)

    submission = ordfm.SystemSubmission.get(submission_info_subgraph,uri="urn:uuid:"+str(system_uuid))
    if submission is None:
        submission = ordfm.SystemSubmission.new(submission_info_subgraph,uri="urn:uuid:"+str(system_uuid))
        submission_info_subgraph.commit()
    else:
        print "Previous submission found. overwriting"
        graphstore.graph().remove_context(rdflib.URIRef("urn:uuid:"+str(system_uuid)))
        graphstore.graph().commit()

    graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+str(options.submission_uuid)))
    system_graph = Graph(graphstore.store(), identifier=rdflib.URIRef("urn:uuid:"+str(system_uuid)))
    print "Adding to graph id urn:uuid:"+str(system_uuid)
    for mol in grrm2.Molecule.all(graph):
        print "-"*40
        print "molecule "+str(mol.uri())

        m = grrm2.Molecule.new(system_graph, mol.uri())
        formula = helperfuncs.generateFormula(mol)
        inchi = helperfuncs.generateInchi(mol)
        smiles = helperfuncs.generateSmiles(mol)
        mass = helperfuncs.generateMass(mol)
        
        print "Formula: "+str(formula)
        print "Inchi: "+str(inchi)
        print "Smiles: "+str(smiles)
        print "Mass: "+str(mass)

        if formula is not None: 
            grrm2.hillFormula(m).set(formula)
        if inchi is not None:
            grrm2.inchi(m).set(inchi)
        if smiles is not None:
            grrm2.smiles(m).set(smiles)
        if mass is not None:
            grrm2.mass(m).set(mass)

        try: 
            helperfuncs.generateMdl(mol)  
        except:
            pass

        canost_planar = helperfuncs.generateCanostPlanar(mol)
        canost_serial = helperfuncs.generateCanostSerial(mol)
        canost_canonical = helperfuncs.generateCanostCanonical(mol)
        print "canost planar: "+str(canost_planar)
        print "canost serial: "+str(canost_serial)
        print "canost canonical: "+str(canost_canonical)

        if canost_planar is not None:
            grrm2.canostPlanar(m).set(canost_planar)
        if canost_serial is not None:
            grrm2.canostSerial(m).set(canost_serial)
        if canost_canonical is not None:
            canost_planar_canonical, canost_serial_canonical = canost_canonical
            if canost_planar_canonical is not None:
                grrm2.canostPlanarCanonical(m).set(canost_planar_canonical)
            if canost_serial_canonical is not None:
                grrm2.canostSerialCanonical(m).set(canost_serial_canonical)

        try:
            helperfuncs.generateMdlForFragments(mol)
        except:
            pass
            
        canost_planar_fragments = helperfuncs.generateCanostPlanarFragments(mol)
        print "canost planar fragments: "+str(canost_planar_fragments)
        if canost_planar_fragments is not None:
            grrm2.fragmentsCanostPlanar(m).set(canost_planar_fragments) 

        canost_serial_fragments = helperfuncs.generateCanostSerialFragments(mol)
        print "canost serial fragments: "+str(canost_serial_fragments)
        if canost_serial_fragments is not None:
            grrm2.fragmentsCanostSerial(m).set(canost_serial_fragments)

        canost_canonical_fragments = helperfuncs.generateCanostCanonicalFragments(mol)
        print "canost canonical fragments: "+str(canost_canonical_fragments)

        if canost_canonical_fragments is not None:
            canost_planar_canonical_fragments=[]
            canost_serial_canonical_fragments=[]

            for fragment_result in canost_canonical_fragments:
                if fragment_result is None:
                    canost_planar_canonical_fragments.append(None)
                    canost_serial_canonical_fragments.append(None)
                    continue
                canost_planar_canonical_fragments.append(fragment_result[0])
                canost_serial_canonical_fragments.append(fragment_result[1])

            print "canost_planar_canonical_fragments : "+str(canost_planar_canonical_fragments)
            print "canost_serial_canonical_fragments : "+str(canost_serial_canonical_fragments)
            grrm2.fragmentsCanostPlanarCanonical(m).set(canost_planar_canonical_fragments)
            grrm2.fragmentsCanostSerialCanonical(m).set(canost_serial_canonical_fragments)

    system_graph.commit()


main()
