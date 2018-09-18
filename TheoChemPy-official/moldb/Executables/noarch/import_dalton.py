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

from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens
from theochempy._theochempy.Chemistry import PeriodicTable
from theochempy._theochempy import Units 

import wavemoldbapi
import getopt
import logging
import tokenfilters
import uuid
import simplejson

class Options:
    def __init__(self): # fold>>
        self.output_filename = None
        self.db_url = None
    # <<fold

def _getOptions(argv): # fold>>
    options = Options()

    opts, args=getopt.getopt(argv[1:], "u:o:hv", ["db-url=", "output=", "help", "verbose"])

    for opt in opts:
        if opt[0] == "-u" or opt[0] == "--db-url":
            if len(opt[1].strip()) == 0:
                _usage("Empty URL in --db-url")
                sys.exit(1)
            options.db_url=opt[1]

        if opt[0] == "-o" or opt[0] == "--output":
            if len(opt[1].strip()) == 0:
                _usage("Empty path in --output")
                sys.exit(1)
            options.output_filename = opt[1].strip()
            
        if opt[0] == "-h" or opt[0] == "--help":
            _usage()
            sys.exit(1)


        if opt[0] == "-v" or opt[0] == "--verbose":
            logging.basicConfig(level=logging.DEBUG)
            
    if options.db_url is None or options.output_filename is None:
        _usage()
        sys.exit(1)
        
    return options
    # <<fold

class DaltonParser:
    def parse(self, output_filename): # fold>>
        logging.debug("Output filename : "+output_filename)

        token_list = Dalton20.tokenizeOutFile(output_filename)

        result = {}
        result["input_molecule"] = None
        result["run_data"] = None
        result["molecules"] = []
        result["triples"] = []
        result["run_data"] = []


        cartesian_coordinates_token = tokenfilters.getCartesianCoordinatesToken(token_list)
        atom_basis_set_token = tokenfilters.getAtomsAndBasisSetsToken(token_list)
        final_geometry_token = tokenfilters.getFinalGeometryToken(token_list)

        if atom_basis_set_token is not None and final_geometry_token is not None:
            final_geometry, triples = self._parseGeometryOptimization(final_geometry_token, atom_basis_set_token)
        
        result["molecules"].append(final_geometry)
        result["triples"].extend(triples)
        return result
        # <<fold

    def _parseGeometryOptimization(self, final_geometry_token, atom_basis_set_token):
        triple_list = []
        current_molecule = {}
        u_id = str(uuid.uuid4())
        current_molecule["uuid"] = u_id
        current_molecule["geometry"] = {}
        current_molecule["geometry"]["symbols"] = []
        current_molecule["geometry"]["labels"] = []
        current_molecule["geometry"]["coordinates"] = []

        for label, symmetry, coords in final_geometry_token.atomList():
            symbol = _labelToElement(label, atom_basis_set_token.atomDataList())
            current_molecule["geometry"]["symbols"].append( symbol )
            current_molecule["geometry"]["labels"].append( label )
            current_molecule["geometry"]["coordinates"].append( coords.asUnit(Units.angstrom).value())


        triple_list.append( ("urn:uuid:"+current_molecule["uuid"] , "http://ontologies.wavemol.org/moldb/v1/#Dalton_ResultType", "ConvergedGeometry"))


        return current_molecule, triple_list
        
def _labelToElement(find_label, datalist): # fold>>
    for t in datalist:
        label, symmetry, atomic_number, basis_expanded, basis_contracted, basis_string = t
        if label == find_label:
            return PeriodicTable.getElementByAtomicNumber(atomic_number).symbol()

    return None
    # <<fold


def _usage(error=None): # fold>>
    print "Usage : "+os.path.basename(sys.argv[0])+" --db-type=type [--simpledb-path=path] --input-type=type filename"
    print ""
    print "--db-url=url"
    print "                The URL of the database to use for import."
    print ""
    print "--output=filename"
    print "                Specifies the filename of the dalton output"
    if error is not None:
        print ""
        print "Error : "+error
        print ""
# <<fold



class DaltonSubmitter:
    def __init__(self, db_url):
        self._db_url = db_url
        
    def submit(self, output_filename):
        logging.debug("Submitting to : "+str(self._db_url))

        db = wavemoldbapi.Wavemoldb(self._db_url)
        run_id = db.create_run(type_uri="http://ontologies.wavemol.org/moldb/v1/types/#Run_Dalton")
        triples = []

        logging.debug("Created new Run: urn:uuid:"+str(run_id))

        result = DaltonParser().parse(output_filename)
        #triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_Job", result["run_data"]["job"] ) )
        #triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_Method", result["run_data"]["method"] ) )
        #triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_BasisSet", result["run_data"]["basis_set"] ) )
        #triples.append( ("urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#GRRM_Options_nrun", result["run_data"]["nrun"] ) )

        #db.update_molecule(result["input_molecule"]["uuid"])
        #print "Created input molecule {"+str(result["input_molecule"]["uuid"])+"}"

        #db.set_run_input(run_id=run_id, input_id = result["input_molecule"]["uuid"])
        #triples.append( ("urn:uuid:"+result["input_molecule"]["uuid"], "http://ontologies.wavemol.org/moldb/v1/#Molecule_Geometry", simplejson.dumps(result["input_molecule"]["geometry"]) ) ) 

        m=result["molecules"][0]
        db.update_molecule(m["uuid"])
        triples.append( ( "urn:uuid:"+m["uuid"], "http://ontologies.wavemol.org/moldb/v1/#Molecule_Geometry", simplejson.dumps(m["geometry"]) ) )
        db.set_run_output(run_id=run_id, output_id = m["uuid"])

        triples.extend(result["triples"])
        print triples
        for t in triples:
            db.insert_triple( *t )
        print "Stored associated information. Done"


def main(argv): # fold>>
    
    options = _getOptions(argv)

    submitter = DaltonSubmitter(options.db_url)
    submitter.submit(options.output_filename)

    # <<fold



if __name__ == "__main__":
    main(sys.argv)
