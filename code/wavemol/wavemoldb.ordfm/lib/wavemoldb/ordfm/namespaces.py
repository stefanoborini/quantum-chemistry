import rdflib

WMOLDB_NS = rdflib.Namespace("http://ontologies.wavemol.org/database/v1/#")

#### will be removed. this is old stuff to be kept for backward compatibility
WM_NS = rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/#")
WMNT_NS = rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/nodetypes/#")
WMRT_NS= rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/runtypes/#")
WMST_NS= rdflib.Namespace("http://ontologies.wavemol.org/moldb/v1/grrm/structuretypes/#")
XSD_NS = rdflib.Namespace("http://www.w3.org/2001/XMLSchema#")
RDF_NS = rdflib.RDF.RDFNS

SPARQL_PREFIX = "PREFIX xsd: "+XSD_NS.n3()+ " PREFIX wm: "+WM_NS.n3()+ " PREFIX wmnt: "+WMNT_NS.n3()+" PREFIX rdf: "+RDF_NS.n3()
