#/usr/bin/env python
# @author Stefano Borini
# @description this script extracts various data from a dalton file and imports it into a
# @description specified database.
# @description It uses TheoChemPy > 0.12.0
# @license Artistic License 2.0

import os
import sys
if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(1,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

from theochempy._theochempy.FileParsers import GRRM
from theochempy._theochempy.FileParsers.GRRM import Tokens as GRRMTokens
from theochempy._theochempy.FileParsers import GRRMInput
from theochempy._theochempy.FileParsers.GRRMInput import Tokens as GRRMInputTokens
from theochempy._theochempy import Units

import uuid
import getopt
import simplejson
import logging

import wavemoldbapi

class Options:
    def __init__(self): # fold>>
        self.db_url = None
        self.grrm_input = None
        self.grrm_EQ = None
        self.grrm_TS = None
        self.grrm_DC = None
        self.grrm_dc = None
    # <<fold 
def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "u:i:e:t:d:c:vh", ["db-url=", "grrm-input=", "grrm-EQ=", "grrm-TS=", "grrm-DC=", "grrm-dc=", "verbose", "help"])

    for opt in opts:
        if opt[0] == "-u" or opt[0] == "--db-url":
            if len(opt[1].strip()) == 0:
                _usage("Empty URL in --db-url")
                sys.exit(1)
            options.db_url=opt[1]

        if opt[0] == "-i" or opt[0] == "--grrm-input":
            if len(opt[1].strip()) == 0:
                _usage("Empty path in --grrm-input")
                sys.exit(1)
            options.grrm_input = opt[1].strip()

        if opt[0] == "-e" or opt[0] == "--grrm-EQ":
            if len(opt[1].strip()) == 0:
                _usage("Empty path in --grrm-EQ")
                sys.exit(1)
            options.grrm_EQ = opt[1].strip()
        if opt[0] == "-t" or opt[0] == "--grrm-TS":
            if len(opt[1].strip()) == 0:
                _usage("Empty path in --grrm-TS")
                sys.exit(1)
            options.grrm_TS = opt[1].strip()

        if opt[0] == "-d" or opt[0] == "--grrm-DC":
            if len(opt[1].strip()) == 0:
                _usage("Empty path in --grrm-DC")
                sys.exit(1)
            options.grrm_DC = opt[1].strip()
 
        if opt[0] == "-c" or opt[0] == "--grrm-dc":
            if len(opt[1].strip()) == 0:
                _usage("Empty path in --grrm-dc")
                sys.exit(1)
            options.grrm_dc = opt[1].strip()
            
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)
        if opt[0] == "-v" or opt[0] == "--verbose":
            logging.basicConfig(level=logging.DEBUG)
            
    if options.db_url is None or options.grrm_input is None or options.grrm_DC is None or options.grrm_EQ is None or options.grrm_TS is None or options.grrm_dc is None:
        _usage()
        sys.exit(1)
    return options
    # <<fold


class GRRMParser:
    def parse(self, input_filename, DC_filename, dc_filename, EQ_filename, TS_filename): # fold>>
        logging.debug("Input filename : "+input_filename)
        logging.debug("DC filename : "+DC_filename)
        logging.debug("dc filename : "+dc_filename)
        logging.debug("EQ filename : "+EQ_filename)
        logging.debug("TS filename : "+TS_filename)

        result = {}
        result["input_molecule"] = None
        result["run_data"] = None
        result["molecules"] = []
        result["triples"] = []
        result["run_data"] = []
        id_to_uuid_mapper = {}
        all_connections = []

        input_molecule, run_data = _parseInputTokenList(GRRMInput.tokenize(input_filename))
        result["input_molecule"] = input_molecule
        result["run_data"] = run_data

        molecules, triples, mapper = _parseDCTokenList(GRRM.tokenizeOutFile(DC_filename))
        result["molecules"].extend(molecules)
        result["triples"].extend(triples)
        id_to_uuid_mapper.update(mapper)

        molecules, triples, mapper, connections = _parsedcTokenList(GRRM.tokenizeOutFile(dc_filename))
        result["molecules"].extend(molecules)
        result["triples"].extend(triples)
        id_to_uuid_mapper.update(mapper)
        all_connections.extend(connections)

        molecules, triples, mapper = _parseEQTokenList(GRRM.tokenizeOutFile(EQ_filename))
        result["molecules"].extend(molecules)
        result["triples"].extend(triples)
        id_to_uuid_mapper.update(mapper)

        molecules, triples, mapper, connections = _parseTSTokenList(GRRM.tokenizeOutFile(TS_filename))
        result["molecules"].extend(molecules)
        result["triples"].extend(triples)
        id_to_uuid_mapper.update(mapper)
        all_connections.extend(connections)
   
        resolved_connection_list = _resolveConnections(all_connections, id_to_uuid_mapper)
        connection_triples = _createConnectionTriples(resolved_connection_list)
        result["triples"].extend(connection_triples)
        return result

    # <<fold

def _resolveConnections(connections, id_to_uuid_mapper): # fold>>
    resolved_connection_list = []
    for source, dest_unresolved in connections:
        dest = id_to_uuid_mapper[dest_unresolved]
        resolved_connection_list.append( (source, dest) )

    return resolved_connection_list
    # <<fold
def _createConnectionTriples(resolved_connection_list): # fold>>
    all_connections_for = {}
    triples = []

    for k, v in resolved_connection_list:
        if not all_connections_for.has_key(k):
            all_connections_for[k] = []
        all_connections_for[k].append(v)
        if not all_connections_for.has_key(v):
            all_connections_for[v] = []
        all_connections_for[v].append(k)

    for k, v in all_connections_for.items():
        triples.append( ("urn:uuid:"+k, 
                         "http://ontologies.wavemol.org/moldb/v1/#GRRM_Connections", 
                         simplejson.dumps(["urn:uuid:"+id for id in v])
                        )
                    )
    return triples
    # <<fold 

def _parseInputTokenList(token_list): # fold>>
    molecule = {}
    run_data = {}

    molecule_uuid = str(uuid.uuid4())

    for t in token_list:
        if t.__class__ == GRRMInputTokens.GeometryToken:
            molecule["uuid"] = molecule_uuid
            molecule["geometry"] = {}
            molecule["geometry"]["labels"] = []
            molecule["geometry"]["symbols"] = []
            molecule["geometry"]["coordinates"] = []
            molecule["charge"] = t.charge()
            molecule["spin"] = t.spin()

            for symbol, coords in t.atomList():
                molecule["geometry"]["labels"].append( symbol )
                molecule["geometry"]["symbols"].append( symbol )
                molecule["geometry"]["coordinates"].append( coords.asUnit(Units.angstrom).value())

        
        if t.__class__ == GRRMInputTokens.NRunOptionToken:
            run_data["nrun"] = t.value()

        if t.__class__ == GRRMInputTokens.CommandDirectiveToken:
            run_data["job"] = t.jobString() 
            run_data["method"] = t.methodString()
            run_data["basis_set"] = t.basisSetString()

    return (molecule, run_data)
# <<fold
def _parseTSTokenList(token_list): # fold>>
    molecule_list = []
    triple_list = []
    structure_type = None
    current_molecule = None
    id_to_uuid_mapper = {}
    connections = []

    if GRRMTokens.HeaderTransitionToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find transition state file Header")

    for t in token_list:
        if t.__class__ == GRRMTokens.StructureHeaderToken:
            current_molecule = {}
            u_id = str(uuid.uuid4())
            current_molecule["uuid"] = u_id
            molecule_list.append(current_molecule)

            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureType", "TS"))
            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureNumber", t.number()))
            id_to_uuid_mapper["TS%d" % t.number()] = u_id

        if t.__class__ == GRRMTokens.GeometryToken:
            current_molecule["geometry"] = {}
            current_molecule["geometry"]["labels"] = []
            current_molecule["geometry"]["symbols"] = []
            current_molecule["geometry"]["coordinates"] = []

            for symbol, coords in t.atomList():
                current_molecule["geometry"]["labels"].append( symbol )
                current_molecule["geometry"]["symbols"].append( symbol )
                current_molecule["geometry"]["coordinates"].append( coords.asUnit(Units.angstrom).value())
        if t.__class__ == GRRMTokens.EnergyToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Energy", t.energy().asUnit(Units.hartree).value()))
        if t.__class__ == GRRMTokens.SpinToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Spin", t.spin().value()))
        if t.__class__ == GRRMTokens.ZPVEToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_ZeroPointVibrationalEnergy", t.zpve().value()))
        if t.__class__ == GRRMTokens.NormalModesToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_NormalModesEigenvalues", simplejson.dumps(t.eigenvalues())))
        if t.__class__ == GRRMTokens.ConnectionToken:
            connections.append( ( current_molecule["uuid"], t.first() ) )
            connections.append( ( current_molecule["uuid"], t.second() ) )

    return (molecule_list, triple_list, id_to_uuid_mapper, connections)
# <<fold
def _parseDCTokenList(token_list): # fold>>
    molecule_list = []
    triple_list = []
    structure_type = None
    current_molecule = None
    id_to_uuid_mapper = {}

    if GRRMTokens.HeaderDissociatedToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find dissociated file Header")

    for t in token_list:
        if t.__class__ == GRRMTokens.StructureHeaderToken:
            current_molecule = {}
            u_id = str(uuid.uuid4())
            current_molecule["uuid"] = u_id
            molecule_list.append(current_molecule)

            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureType", "DC"))
            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureNumber", t.number()))
            id_to_uuid_mapper["DC%d" % t.number()] = u_id

        if t.__class__ == GRRMTokens.GeometryToken:
            current_molecule["geometry"] = {}
            current_molecule["geometry"]["labels"] = []
            current_molecule["geometry"]["symbols"] = []
            current_molecule["geometry"]["coordinates"] = []

            for symbol, coords in t.atomList():
                current_molecule["geometry"]["labels"].append( symbol )
                current_molecule["geometry"]["symbols"].append( symbol )
                current_molecule["geometry"]["coordinates"].append( coords.asUnit(Units.angstrom).value())
        if t.__class__ == GRRMTokens.EnergyToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Energy", t.energy().asUnit(Units.hartree).value()))
        if t.__class__ == GRRMTokens.SpinToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Spin", t.spin().value()))
        if t.__class__ == GRRMTokens.ZPVEToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_ZeroPointVibrationalEnergy", t.zpve().value()))
        if t.__class__ == GRRMTokens.NormalModesToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_NormalModesEigenvalues", simplejson.dumps(t.eigenvalues())))
    return (molecule_list, triple_list, id_to_uuid_mapper)
# <<fold
def _parsedcTokenList( token_list): # fold>>
    molecule_list = []
    triple_list = []
    structure_type = None
    current_molecule = None
    id_to_uuid_mapper = {}
    connections = []

    if GRRMTokens.HeaderDissociatedToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find dissociated file Header")

    for t in token_list:
        if t.__class__ == GRRMTokens.StructureHeaderToken:
            current_molecule = {}
            u_id = str(uuid.uuid4())
            current_molecule["uuid"] = u_id
            molecule_list.append(current_molecule)

            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureType", "dc"))
            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureNumber", t.number()))
            id_to_uuid_mapper["dc%d" % t.number()] = u_id

        if t.__class__ == GRRMTokens.GeometryToken:
            current_molecule["geometry"] = {}
            current_molecule["geometry"]["labels"] = []
            current_molecule["geometry"]["symbols"] = []
            current_molecule["geometry"]["coordinates"] = []

            for symbol, coords in t.atomList():
                current_molecule["geometry"]["labels"].append( symbol )
                current_molecule["geometry"]["symbols"].append( symbol )
                current_molecule["geometry"]["coordinates"].append( coords.asUnit(Units.angstrom).value())
        if t.__class__ == GRRMTokens.EnergyToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Energy", t.energy().asUnit(Units.hartree).value()))
        if t.__class__ == GRRMTokens.SpinToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Spin", t.spin().value()))
        if t.__class__ == GRRMTokens.ZPVEToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_ZeroPointVibrationalEnergy", t.zpve().value()))
        if t.__class__ == GRRMTokens.NormalModesToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_NormalModesEigenvalues", simplejson.dumps(t.eigenvalues())))

        if t.__class__ == GRRMTokens.ConnectionToken:
            connections.append( ( current_molecule["uuid"], "EQ"+str(t.first()) ) )

    return (molecule_list, triple_list, id_to_uuid_mapper, connections)
# <<fold
def _parseEQTokenList(token_list): # fold>>
    molecule_list = []
    triple_list = []
    structure_type = None
    current_molecule = None
    id_to_uuid_mapper = {}

    if GRRMTokens.HeaderEquilibriumToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find equilibrium file Header")

    for t in token_list:
        if t.__class__ == GRRMTokens.StructureHeaderToken:
            current_molecule = {}
            u_id = str(uuid.uuid4())
            current_molecule["uuid"] = u_id
            molecule_list.append(current_molecule)

            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureType", "EQ"))
            triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#GRRM_StructureNumber", t.number()))
            id_to_uuid_mapper["EQ%d" % t.number()] = u_id

        if t.__class__ == GRRMTokens.GeometryToken:
            current_molecule["geometry"] = {}
            current_molecule["geometry"]["labels"] = []
            current_molecule["geometry"]["symbols"] = []
            current_molecule["geometry"]["coordinates"] = []

            for symbol, coords in t.atomList():
                current_molecule["geometry"]["labels"].append( symbol )
                current_molecule["geometry"]["symbols"].append( symbol )
                current_molecule["geometry"]["coordinates"].append( coords.asUnit(Units.angstrom).value())
        if t.__class__ == GRRMTokens.EnergyToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Energy", t.energy().asUnit(Units.hartree).value()))
        if t.__class__ == GRRMTokens.SpinToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_Spin", t.spin().value()))
        if t.__class__ == GRRMTokens.ZPVEToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_ZeroPointVibrationalEnergy", t.zpve().value()))
        if t.__class__ == GRRMTokens.NormalModesToken:
            triple_list.append(("urn:uuid:"+current_molecule["uuid"], "http://ontologies.wavemol.org/moldb/v1/#GRRM_NormalModesEigenvalues", simplejson.dumps(t.eigenvalues())))
    return (molecule_list, triple_list, id_to_uuid_mapper)
# <<fold

class GRRMSubmitter:
    def __init__(self, db_url):
        self._db_url = db_url
        
    def submit(self, grrm_input, grrm_DC, grrm_dc, grrm_EQ, grrm_TS):
        print "Submitting to : "+str(self._db_url)

        db = wavemoldbapi.Wavemoldb(self._db_url)
        run_id = db.create_run(type_uri="http://ontologies.wavemol.org/moldb/v1/types/#Run_GRRM")
        triples = []

        logging.debug("Importing new Run: urn:uuid:"+run_id)
        print "Created new Run {"+str(run_id)+"}"

        result = GRRMParser().parse(grrm_input,grrm_DC,grrm_dc,grrm_EQ,grrm_TS)
        triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_Job", result["run_data"]["job"] ) )
        triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_Method", result["run_data"]["method"] ) )
        triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_BasisSet", result["run_data"]["basis_set"] ) )
        triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_Options_nrun", result["run_data"]["nrun"] ) )

        db.update_molecule(result["input_molecule"]["uuid"])
        print "Created input molecule {"+str(result["input_molecule"]["uuid"])+"}"

        db.set_run_input(run_id=run_id, input_id = result["input_molecule"]["uuid"])
        triples.append( ("urn:uuid:"+result["input_molecule"]["uuid"], "http://ontologies.wavemol.org/moldb/v1/#Molecule_Geometry", simplejson.dumps(result["input_molecule"]["geometry"]) ) ) 
        triples.append( ("urn:uuid:"+result["input_molecule"]["uuid"], "http://ontologies.wavemol.org/moldb/v1/#Molecule_Spin", result["input_molecule"]["spin"] ) )
        triples.append( ("urn:uuid:"+result["input_molecule"]["uuid"], "http://ontologies.wavemol.org/moldb/v1/#Molecule_Charge", result["input_molecule"]["charge"] ) )

        for m in result["molecules"]:
            db.update_molecule(m["uuid"])
            triples.append( ( "urn:uuid:"+m["uuid"], "http://ontologies.wavemol.org/moldb/v1/#Molecule_Geometry", simplejson.dumps(m["geometry"]) ) )

        output_collection_id = db.create_collection(content=[ m["uuid"] for m in result["molecules"]])
        print "Created output collection {"+output_collection_id+"}, containing "+str(len([ m["uuid"] for m in result["molecules"]]))+" molecules"

        db.set_run_output(run_id=run_id, output_id = output_collection_id)

        triples.extend(result["triples"])
        for t in triples:
            db.insert_triple( *t )
        print "Stored associated information. Done"


def _usage(error=None): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" options"
    print ""
    print "--verbose"
    print "                Be verbose (for debug)"
    print "--db-url=URL"
    print "                The base URL database to use for import."
    print ""
    print "--grrm-input=filename"
    print "--grrm-EQ=filename"
    print "--grrm-TS=filename"
    print "--grrm-DC=filename"
    print "--grrm-dc=filename"
    print "                the filenames of the input, equilibrium (EQ), transition state (TS)"
    print "                and dissociated (DC and dc) structure"
    print ""
    if error is not None:
        print ""
        print "Error : "+error
        print ""
# <<fold

def main(argv): # fold>>
    
    options = _getOptions(argv)

    submitter = GRRMSubmitter(options.db_url)
    submitter.submit(options.grrm_input, options.grrm_DC, options.grrm_dc, options.grrm_EQ, options.grrm_TS)
         
    # <<fold



if __name__ == "__main__":
    main(sys.argv)
