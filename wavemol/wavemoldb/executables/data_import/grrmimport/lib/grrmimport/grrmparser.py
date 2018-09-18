import sys
from wavemoldb.ordfm import grrm2
from . import uuid
from . import printout
from . import parsinghelpers

import rdflib
import types
import os
import re

            
def _isComplete(dictionary):
    """check if a dictionary having as a key an integer is complete or there's a missing key"""
   
    if False in map(lambda x: type(x) == types.IntType, dictionary.keys()):
        raise TypeError()
    
    for i in xrange(0, max(dictionary.keys())+1):
        if not dictionary.has_key(i):
            return False

    return True
        

class Anon: pass


class GRRMParser:
    def __init__(self):
        self._files = None
        self._grrm_dir = None
        self._graph = rdflib.ConjunctiveGraph(identifier = rdflib.URIRef("urn:uuid:"+str(uuid.uuid4())))
        self._all_parsers = None
        
    def parse(self, grrm_dir): # fold>>
        self._grrm_dir = grrm_dir
        self._getFiles() 
        self._checkFileSanity() # mine is gone long ago
        self._getAllParsers()
        printout.keyvalue("run_uri", self._all_parsers.input.run().uri())
        outputs = self._getAllOutputs()
        for o in outputs:
            grrm2.runOutput(self._all_parsers.input.run()).add(o)

        self._resolveLinking()
        return self._graph 

    def _resolveLinking(self):
        # the information we currently have is lacking mapping of structures. We only have structure type/number (TS 1, EQ 2 etc.) associations
        # and a bunch of uuid, one for each molecule. We need to create the links by mapping the structure type/number to the corresponding
        # uuids
        mapper = self._getMapper()
        cr = parsinghelpers.ConnectionResolver(self._graph, self._all_parsers, mapper)

    def _getAllOutputs(self):
        all_output = []
        all_output.extend(self._all_parsers.UDC.molecules())
        all_output.extend(self._all_parsers.DDC.molecules())
        all_output.extend(self._all_parsers.EQ.molecules())
        all_output.extend(self._all_parsers.TS.molecules())

        for ts_analysis in self._all_parsers.TSAnalysis_d.values():
            all_output.extend(ts_analysis.interconversionSteps()[0])
            all_output.extend(ts_analysis.interconversionSteps()[1])
            all_output.extend(ts_analysis.interconversions())
        for udc_analysis in self._all_parsers.UDCAnalysis_d.values():
            all_output.extend(udc_analysis.interconversionSteps()[0])
            all_output.extend(udc_analysis.interconversions())
        return all_output

    def _getMapper(self):
        all_connections = self._all_parsers.UDC.connections() + self._all_parsers.TS.connections()
        
        structure_label_to_molecule_mapper = {}
        structure_label_to_molecule_mapper.update(self._all_parsers.UDC.structureLabelToMoleculeMapper())
        structure_label_to_molecule_mapper.update(self._all_parsers.DDC.structureLabelToMoleculeMapper())
        structure_label_to_molecule_mapper.update(self._all_parsers.EQ.structureLabelToMoleculeMapper())
        structure_label_to_molecule_mapper.update(self._all_parsers.TS.structureLabelToMoleculeMapper())

        all_interconversion_additional_infos= []
        for parser in self._all_parsers.TSAnalysis_d.values() +  self._all_parsers.UDCAnalysis_d.values():
            all_interconversion_additional_infos.extend(parser.interconversionAdditionalInfos())
             
        return parsinghelpers.ConnectionMapper(all_connections, structure_label_to_molecule_mapper, all_interconversion_additional_infos)

    def _getAllParsers(self):
        graph = self._graph
        self._all_parsers = Anon()
        self._all_parsers.input = parsinghelpers.InputFileParser(graph, self._files["input"])
        self._all_parsers.UDC = parsinghelpers.OutputUDCFileParser(graph, self._files["uDC_list"])
        self._all_parsers.DDC = parsinghelpers.OutputDDCFileParser(graph, self._files["dDC_list"])
        self._all_parsers.EQ = parsinghelpers.OutputEQFileParser(graph, self._files["EQ_list"])
        self._all_parsers.TS = parsinghelpers.OutputTSFileParser(graph, self._files["TS_list"])
        
        self._all_parsers.TSAnalysis_d = {}
        for number, ts_file in self._files["TSn_log"].items():
            self._all_parsers.TSAnalysis_d[number] = parsinghelpers.TSAnalysisParser(graph, ts_file)

        self._all_parsers.UDCAnalysis_d = {}
        for number, udc_file in self._files["uDCn_log"].items():
            self._all_parsers.UDCAnalysis_d[number] = parsinghelpers.UDCAnalysisParser(graph, udc_file)

    def _getFiles(self):
        def isInputFile(fname):
            base, ext = os.path.splitext(fname)
            if ext == ".com" and "GauJob" not in base:
                return True
            return False

        file_list = os.listdir(self._grrm_dir)
        input = filter(isInputFile, file_list )

        if len(input) != 1:
            raise ValueError("input file list does not contain one element. Found "+len(input) )
        input_file = input[0]
        input_prefix = os.path.splitext(input_file)[0]

        d = {}
        d["input"] = None
        d["unknown"] = []
        d["TS_list"] = None
        d["EQ_list"] = None
        d["dDC_list"] = None
        d["uDC_list"] = None
        d["uDCn_log"] = {}
        d["TSn_log"] = {}

        for f in file_list:
            m_TS = re.match(input_prefix+"_TS(\d+)\.log", f)
            m_uDC = re.match(input_prefix+"_uDC(\d+)\.log", f)

            if f == input_file:
                d["input"] = os.path.join(self._grrm_dir,f)
            elif f == input_prefix+"_TS_list.log":
                if d["TS_list"] is not None:
                    raise ValueError("Multiple TS_list file found")
                d["TS_list"] = os.path.join(self._grrm_dir,f)
            elif f == input_prefix+"_dDC_list.log":
                if d["dDC_list"] is not None:
                    raise ValueError("Multiple dDC_list file found")
                d["dDC_list"] =  os.path.join(self._grrm_dir,f)
            elif f == input_prefix+"_uDC_list.log":
                if d["uDC_list"] is not None:
                    raise ValueError("Multiple uDC_list file found")
                d["uDC_list"] = os.path.join(self._grrm_dir,f)
            elif f == input_prefix+"_EQ_list.log":
                if d["EQ_list"] is not None:
                    raise ValueError("Multiple EQ_list file found")
                d["EQ_list"] = os.path.join(self._grrm_dir,f)
            elif m_TS:
                d["TSn_log"][int(m_TS.group(1))] = os.path.join(self._grrm_dir, m_TS.group(0))
            elif m_uDC:
                d["uDCn_log"][int(m_uDC.group(1))] = os.path.join(self._grrm_dir, m_uDC.group(0))
            else:
                d["unknown"].append(os.path.join(self._grrm_dir,f))
        
        self._files = d

    def _checkFileSanity(self):
        files = self._files

        printout.keyvalue("input_file", files["input"])
        printout.keyvalue("uDC_list", files["uDC_list"])
        printout.keyvalue("dDC_list", files["dDC_list"])
        printout.keyvalue("TS_list", files["TS_list"])
        printout.keyvalue("TSn_log", files["TSn_log"])
        printout.keyvalue("uDCn_log", files["uDCn_log"])
        printout.keyvalue("unknown", files["unknown"])

        if None in [files["input"], files["dDC_list"], files["uDC_list"], files["EQ_list"], files["TS_list"]]:
            raise Exception("missing file")

        if not _isComplete(files["TSn_log"]):
            raise Exception("incomplete TSn_log")
            
        if not _isComplete(files["uDCn_log"]):
            raise Exception("incomplete uDCn_log")


