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

from wavemol.parsers import grrm
from wavemol.parsers.grrm import tokentypes
from wavemol.core import units

import uuid
import getopt
import simplejson
import logging
import httpcomm

import rdflib

WM_NS = rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/#")
WMNT_NS = rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/nodetypes/#")
WMRT_NS = rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/runtypes/#")
XSD_NS = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")
RDF_NS = rdflib.RDF.RDFNS


class Options:
    def __init__(self, argv): # fold>>
        self.db_url = None
        self.output = None
        self.grrm_input = None
        self.grrm_EQ = None
        self.grrm_TS = None
        self.grrm_DC = None
        self.grrm_dc = None
        self._getOptions(argv)
    # <<fold 
    
    def _getOptions(self,argv): # fold>>
        
        opts, args=getopt.getopt(argv[1:], "u:o:i:e:t:d:c:p:Pvh", ["db-url=", "output=", "grrm-input=", "grrm-EQ=", "grrm-TS=", "grrm-DC=", "grrm-dc=", "verbose", "help"])

        for opt in opts:
            db_url = self._getOptionArg(opt, "-u","--db-url")
            if db_url:
                self.db_url = db_url

            output = self._getOptionArg(opt, "-o","--output")
            if output:
                self.output = output

            grrm_input = self._getOptionArg(opt, "-i", "--grrm-input")
            if grrm_input:
                self.grrm_input = grrm_input

            grrm_EQ = self._getOptionArg(opt, "-e","--grrm-EQ")
            if grrm_EQ:
                self.grrm_EQ = grrm_EQ

            grrm_TS = self._getOptionArg(opt, "-t","--grrm-TS")
            if grrm_TS:
                self.grrm_TS = grrm_TS

            grrm_DC = self._getOptionArg(opt, "-d","--grrm-DC")
            if grrm_DC:
                self.grrm_DC = grrm_DC

            grrm_dc = self._getOptionArg(opt, "-c","--grrm-dc")
            if grrm_dc:
                self.grrm_dc = grrm_dc

            if opt[0] in ["-h", "--help"]:
                _usage()
                sys.exit(1)
            if opt[0] in [ "-v", "--verbose"]:
                logging.basicConfig(level=logging.DEBUG)
                
        if None in [self.grrm_input, self.grrm_DC, self.grrm_EQ, self.grrm_TS, self.grrm_dc]:
            _usage("Required information missing : GRRM files")
            sys.exit(1)

        if self.db_url is None and self.output is None:
            _usage("Required information missing : target file/database url")
            sys.exit(1)
            
        # <<fold
    def _getOptionArg(self, opt, short, long, not_empty=True):
        if opt[0] in [short, long]:
            if len(opt[1].strip()) == 0 and not_empty:
                _usage("Empty value in "+short+"/"+long)
                sys.exit(1)
            return opt[1].strip()
        return None
       

def _parseGeometryToken(token): # fold>>
    geometry = {}
    geometry["labels"] = []
    geometry["symbols"] = []
    geometry["coordinates"] = []

    for symbol, coords in token.atomList():
        coords.units = units.angstrom
        geometry["labels"].append( symbol )
        geometry["symbols"].append( symbol )
        geometry["coordinates"].append(list(coords.magnitude))

    return geometry
    # <<fold
def _parseEnergyToken(token): # fold>>
    energy = token.energy()
    energy.units = units.hartree
    return float(energy.magnitude)
    # <<fold
def _parseZPVEToken(token): # fold>>
    zpve = token.zpve()
    zpve.units = units.hartree
    return float(zpve.magnitude)
    # <<fold
def _parseNormalModesEigenvalues(token): # fold>>
    def _convert(value):
        value.units = units.hartree
        return float(value.magnitude)

    eig = token.eigenvalues()
    return simplejson.dumps(map(_convert, eig))
    # <<fold

class GRRMParser:
    def __init__(self):
        pass
    def parse(self, input_filename, DC_filename, dc_filename, EQ_filename, TS_filename): # fold>>
        triples = []
        graph = rdflib.ConjunctiveGraph(identifier = rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        id_to_uuid_mapper = {}

        logging.debug("Input filename : "+input_filename)
        logging.debug("DC filename : "+DC_filename)
        logging.debug("dc filename : "+dc_filename)
        logging.debug("EQ filename : "+EQ_filename)
        logging.debug("TS filename : "+TS_filename)
        
        run_id = str(uuid.uuid4())

        print "Importing new Run urn:uuid:"+run_id

        triples.append( ( rdflib.URIRef("urn:uuid:"+run_id), RDF_NS.type, WMNT_NS.Run) )

        input_tokenizer = grrm.GRRMInputTokenizer()
        result = _parseInputTokenList(run_id, list(input_tokenizer.tokenize(input_filename)))
        
        triples.extend(result["triples"])
        triples.append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.Run_Input, rdflib.URIRef("urn:uuid:"+result["molecule_uuid"])) )

        output_tokenizer = grrm.GRRMOutputTokenizer()
        DC_result = _parseDCTokenList(list(output_tokenizer.tokenize(DC_filename)))
        dc_result = _parsedcTokenList(list(output_tokenizer.tokenize(dc_filename)))
        EQ_result = _parseEQTokenList(list(output_tokenizer.tokenize(EQ_filename)))
        TS_result = _parseTSTokenList(list(output_tokenizer.tokenize(TS_filename)))

        triples.extend(DC_result["triples"])
        triples.extend(dc_result["triples"])
        triples.extend(EQ_result["triples"])
        triples.extend(TS_result["triples"])

        all_connections = dc_result["connections"]+TS_result["connections"]
        id_to_uuid_mapper = {}
        id_to_uuid_mapper.update(DC_result["id_to_uuid_mapper"])
        id_to_uuid_mapper.update(dc_result["id_to_uuid_mapper"])
        id_to_uuid_mapper.update(EQ_result["id_to_uuid_mapper"])
        id_to_uuid_mapper.update(TS_result["id_to_uuid_mapper"])

        resolved_connection_list = _resolveConnections(all_connections, id_to_uuid_mapper)
        triples.extend(_createConnectionTriples(resolved_connection_list))


        collection_uuid = str(uuid.uuid4())
        triples.append( ( rdflib.URIRef("urn:uuid:"+collection_uuid), RDF_NS.type, WMNT_NS.Collection) )
        bag = rdflib.BNode()
        triples.append( ( bag, RDF_NS.type, RDF_NS.Bag) )
        triples.append( ( rdflib.URIRef("urn:uuid:"+collection_uuid), WM_NS.Collection_Contents, bag) )

        for i,c in enumerate( DC_result["molecules_uuid_list"]+dc_result["molecules_uuid_list"]+EQ_result["molecules_uuid_list"]+TS_result["molecules_uuid_list"] ):
            triples.append( ( bag, RDF_NS["_"+str(i+1)], rdflib.URIRef("urn:uuid:"+c)) )

        triples.append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.Run_Output, rdflib.URIRef("urn:uuid:"+collection_uuid)) )

        for t in triples:
            graph.add(t)

        return graph

    # <<fold

def _parseInputTokenList(run_id, token_list): # fold>>
    result = {}
    result["molecule_uuid"] = None
    result["triples"] = []

    molecule = {}
    run_data = {}

    molecule_uuid = str(uuid.uuid4())
    result["molecule_uuid"] = molecule_uuid
    result["triples"].append( ( rdflib.URIRef('urn:uuid:'+molecule_uuid), RDF_NS.type, WMNT_NS.Molecule) )

    for t in token_list:
        if t.__class__ == tokentypes.InputGeometryToken:
            molecule["charge"] = int(t.charge())
            molecule["spin"] = int(t.spin())
            molecule["geometry"] = _parseGeometryToken(t)
        elif t.__class__ == tokentypes.NRunOptionToken:
            run_data["nrun"] = int(t.value())
        elif t.__class__ == tokentypes.CommandDirectiveToken:
            run_data["job"] = t.jobString() 
            run_data["method"] = t.methodString()
            run_data["basis_set"] = t.basisSetString()

    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+molecule_uuid), RDF_NS.type, rdflib.URIRef(WMNT_NS.Molecule) ))
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+molecule_uuid), WM_NS.Molecule_Geometry, rdflib.Literal(simplejson.dumps(molecule["geometry"])) ) ) 
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+molecule_uuid), WM_NS.Molecule_Spin, rdflib.Literal(molecule["spin"] ) ) )
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+molecule_uuid), WM_NS.Molecule_Charge, rdflib.Literal(molecule["charge"] ) ) )

    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.Run_Type, WMRT_NS.GRRM ) )
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.GRRM_Job, rdflib.Literal(run_data["job"]) ) )
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.GRRM_Method, rdflib.Literal(run_data["method"]) ) )
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.GRRM_BasisSet, rdflib.Literal(run_data["basis_set"]) ) )
    result["triples"].append( ( rdflib.URIRef("urn:uuid:"+run_id), WM_NS.GRRM_Options_nrun, rdflib.Literal(run_data["nrun"]) ) )
    return result

    # <<fold
def _parseTSTokenList(token_list): # fold>>
    result={}
    result["triples"] = []
    result["id_to_uuid_mapper"] = {}
    result["connections"] = []
    result["molecules_uuid_list"] = []

    current_molecule = None
    molecule_list = []

    if tokentypes.HeaderTransitionToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find transition state file Header")

    for t in token_list:
        if t.__class__ == tokentypes.StructureHeaderToken:
            current_molecule = {}
            molecule_list.append(current_molecule)
            molecule_uuid = str(uuid.uuid4())
            current_molecule["uuid"] = molecule_uuid
            current_molecule["structure_type"] = "TS"
            current_molecule["structure_number"] = int(t.number())

            result["molecules_uuid_list"].append(molecule_uuid)
            result["id_to_uuid_mapper"]["TS%d" % t.number()] = molecule_uuid

        if t.__class__ == tokentypes.GeometryToken:
            current_molecule["geometry"] = _parseGeometryToken(t)
        if t.__class__ == tokentypes.EnergyToken:
            current_molecule["energy"] = _parseEnergyToken(t)
        if t.__class__ == tokentypes.SpinToken:
            current_molecule["spin"] = int(t.spin().magnitude)
        if t.__class__ == tokentypes.ZPVEToken:
            current_molecule["zpve"] = _parseZPVEToken(t)
        if t.__class__ == tokentypes.NormalModesToken:
            current_molecule["normalmodes"] = _parseNormalModesEigenvalues(t)
        if t.__class__ == tokentypes.ConnectionToken:
            result["connections"].append( ( current_molecule["uuid"], t.first() ) )
            result["connections"].append( ( current_molecule["uuid"], t.second() ) )


    for m in molecule_list:
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), RDF_NS.type, rdflib.URIRef(WMNT_NS.Molecule) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureType, rdflib.Literal(m["structure_type"]) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureNumber, rdflib.Literal(m["structure_number"]) ) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.Molecule_Geometry, rdflib.Literal(simplejson.dumps(m["geometry"])) ) ) 
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Energy, rdflib.Literal(m["energy"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Spin, rdflib.Literal(m["spin"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_ZeroPointVibrationalEnergy, rdflib.Literal(m["zpve"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_NormalModesEigenvalues, rdflib.Literal(m["normalmodes"]) ) )


    return result
# <<fold
def _parseDCTokenList(token_list): # fold>>
    result = {}
    result["triples"] = []
    result["id_to_uuid_mapper"] = {}
    result["molecules_uuid_list"] = []

    molecule_list = []
    current_molecule = None

    if tokentypes.HeaderDissociatedToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find dissociated file Header")

    for t in token_list:
        if t.__class__ == tokentypes.StructureHeaderToken:
            current_molecule = {}
            molecule_list.append(current_molecule)
            molecule_uuid = str(uuid.uuid4())
            current_molecule["uuid"] = molecule_uuid
            current_molecule["structure_type"] = "DC"
            current_molecule["structure_number"] = int(t.number())
            
            result["molecules_uuid_list"].append(molecule_uuid)
            result["id_to_uuid_mapper"]["DC%d" % t.number()] = molecule_uuid

        if t.__class__ == tokentypes.GeometryToken:
            current_molecule["geometry"] = _parseGeometryToken(t)
        if t.__class__ == tokentypes.EnergyToken:
            current_molecule["energy"] = _parseEnergyToken(t)
        if t.__class__ == tokentypes.SpinToken:
            current_molecule["spin"] = int(t.spin().magnitude)
        if t.__class__ == tokentypes.ZPVEToken:
            current_molecule["zpve"] = _parseZPVEToken(t)
        if t.__class__ == tokentypes.NormalModesToken:
            current_molecule["normalmodes"] = _parseNormalModesEigenvalues(t)

    for m in molecule_list:
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), RDF_NS.type, rdflib.URIRef(WMNT_NS.Molecule) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureType, rdflib.Literal(m["structure_type"]) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureNumber, rdflib.Literal(m["structure_number"]) ) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.Molecule_Geometry, rdflib.Literal(simplejson.dumps(m["geometry"])) ) ) 
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Energy, rdflib.Literal(m["energy"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Spin, rdflib.Literal(m["spin"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_ZeroPointVibrationalEnergy, rdflib.Literal(m["zpve"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_NormalModesEigenvalues, rdflib.Literal(m["normalmodes"]) ) )

    return result
# <<fold
def _parsedcTokenList(token_list): # fold>>
    result={}
    result["triples"] = []
    result["id_to_uuid_mapper"] = {}
    result["connections"] = []
    result["molecules_uuid_list"] = []

    current_molecule = None
    molecule_list = []

    if tokentypes.HeaderDissociatedToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find dissociated file Header")

    for t in token_list:
        if t.__class__ == tokentypes.StructureHeaderToken:
            current_molecule = {}
            molecule_list.append(current_molecule)
            molecule_uuid = str(uuid.uuid4())
            current_molecule["uuid"] = molecule_uuid
            current_molecule["structure_type"] = "dc"
            current_molecule["structure_number"] = int(t.number())

            result["molecules_uuid_list"].append(molecule_uuid)
            result["id_to_uuid_mapper"]["dc%d" % t.number()] = molecule_uuid
    
        if t.__class__ == tokentypes.GeometryToken:
            current_molecule["geometry"] = _parseGeometryToken(t)
        if t.__class__ == tokentypes.EnergyToken:
            current_molecule["energy"] = _parseEnergyToken(t)
        if t.__class__ == tokentypes.SpinToken:
            current_molecule["spin"] = int(t.spin())
        if t.__class__ == tokentypes.ZPVEToken:
            current_molecule["zpve"] = _parseZPVEToken(t)
        if t.__class__ == tokentypes.NormalModesToken:
            current_molecule["normalmodes"] = _parseNormalModesEigenvalues(t)
        if t.__class__ == tokentypes.ConnectionToken:
            result["connections"].append( ( current_molecule["uuid"], "EQ"+str(t.first()) ) )

    for m in molecule_list:
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), RDF_NS.type, rdflib.URIRef(WMNT_NS.Molecule) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureType, rdflib.Literal(m["structure_type"]) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureNumber, rdflib.Literal(m["structure_number"]) ) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.Molecule_Geometry, rdflib.Literal(simplejson.dumps(m["geometry"])) ) ) 
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Energy, rdflib.Literal(m["energy"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Spin, rdflib.Literal(m["spin"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_ZeroPointVibrationalEnergy, rdflib.Literal(m["zpve"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_NormalModesEigenvalues, rdflib.Literal(m["normalmodes"]) ) )

    return result
# <<fold
def _parseEQTokenList(token_list): # fold>>
    result={}
    result["triples"] = []
    result["id_to_uuid_mapper"] = {}
    result["molecules_uuid_list"] = []

    current_molecule = None
    molecule_list = []

    if tokentypes.HeaderEquilibriumToken not in [t.__class__ for t in token_list]:
        raise Exception("Unable to find equilibrium file Header")

    for t in token_list:
        if t.__class__ == tokentypes.StructureHeaderToken:
            current_molecule = {}
            molecule_list.append(current_molecule)
            molecule_uuid = str(uuid.uuid4())
            current_molecule["uuid"] = molecule_uuid
            current_molecule["structure_type"] = "EQ"
            current_molecule["structure_number"] = int(t.number())

            result["molecules_uuid_list"].append(molecule_uuid)
            result["id_to_uuid_mapper"]["EQ%d" % t.number()] = molecule_uuid

        if t.__class__ == tokentypes.GeometryToken:
            current_molecule["geometry"] = _parseGeometryToken(t)
        if t.__class__ == tokentypes.EnergyToken:
            current_molecule["energy"] = _parseEnergyToken(t)
        if t.__class__ == tokentypes.SpinToken:
            current_molecule["spin"] = int(t.spin())
        if t.__class__ == tokentypes.ZPVEToken:
            current_molecule["zpve"] = _parseZPVEToken(t)
        if t.__class__ == tokentypes.NormalModesToken:
            current_molecule["normalmodes"] = _parseNormalModesEigenvalues(t)

    for m in molecule_list:
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), RDF_NS.type, rdflib.URIRef(WMNT_NS.Molecule) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureType, rdflib.Literal(m["structure_type"]) ))
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_StructureNumber, rdflib.Literal(m["structure_number"]) ) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.Molecule_Geometry, rdflib.Literal(simplejson.dumps(m["geometry"])) ) ) 
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Energy, rdflib.Literal(m["energy"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_Spin, rdflib.Literal(m["spin"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_ZeroPointVibrationalEnergy, rdflib.Literal(m["zpve"])) )
        result["triples"].append( ( rdflib.URIRef("urn:uuid:"+m["uuid"]), WM_NS.GRRM_NormalModesEigenvalues, rdflib.Literal(m["normalmodes"]) ) )

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

    for subject, connections in all_connections_for.items():
        bag = rdflib.BNode()
        triples.append( ( rdflib.URIRef("urn:uuid:"+subject), WM_NS.GRRM_Connections, bag ) )
        triples.append( ( bag, RDF_NS.type, RDF_NS.Bag) )
        for i,c in enumerate(connections):
            triples.append( ( bag, RDF_NS["_"+str(i+1)], rdflib.URIRef("urn:uuid:"+c)) )
            

    return triples
    # <<fold 

class GRRMFileSubmitter:
    def __init__(self, filename):
        self._filename = filename

    def submit(self, grrm_input, grrm_DC, grrm_dc, grrm_EQ, grrm_TS):
        print "Storing into file : "+str(self._filename)

        graph = GRRMParser().parse(grrm_input,grrm_DC,grrm_dc,grrm_EQ,grrm_TS)
        rdf_data = graph.serialize()
        f=file(self._filename,"w")
        f.write(rdf_data)
        f.close()
        print "Done."
            
class GRRMHttpSubmitter:
    def __init__(self, db_url):
        self._db_url = db_url
        
    def submit(self, grrm_input, grrm_DC, grrm_dc, grrm_EQ, grrm_TS):
        print "Submitting to URL : "+str(self._db_url)

        graph = GRRMParser().parse(grrm_input,grrm_DC,grrm_dc,grrm_EQ,grrm_TS)

        rdf_data = graph.serialize()
        status, message, payload = httpcomm.posturl(self._db_url+"/api/v2/triples", [ ("xml", rdf_data) ], [] )
        print "status : "+str(status)
        print "message : "+message
        print "payload : "+payload
        print "Done."

def _usage(error=None): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" options"
    print ""
    print "--verbose"
    print "                Be verbose (for debug)"
    print "--db-url=URL"
    print "                The base URL database to use for import."
    print "--output=file.xml"
    print "                Writes the final RDF representation to file.xml"
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
    
    options = Options(argv)

    submitters = []

    if options.db_url:
        submitters.append( GRRMHttpSubmitter(options.db_url) )

    if options.output:
        submitters.append( GRRMFileSubmitter(options.output) )
        
    for s in submitters:     
        s.submit(options.grrm_input, options.grrm_DC, options.grrm_dc, options.grrm_EQ, options.grrm_TS)
    # <<fold


if __name__ == "__main__":
    main(sys.argv)
