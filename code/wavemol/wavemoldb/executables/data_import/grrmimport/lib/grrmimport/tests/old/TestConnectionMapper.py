# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
from grrmimport import parsinghelpers
import unittest
from grrmimport.parsinghelpers.ConnectionRouteAdditionalInfo import ConnectionRouteAdditionalInfo

class TestConnectionMapper(unittest.TestCase):
    def testConnectionMapper(self): 
        all_connections = [ 
                            ( ("EQ", 1), ("TS", 1) ),
                            ( ("TS", 1), ("EQ", 2) ), 
                            ]
        structure_label_to_uri_mapper = { ("EQ", 1) : "urn:uuid:foo",
                                          ("EQ", 2) : "urn:uuid:bar",
                                          ("TS", 1) : "urn:uuid:baz",
                                          }

        all_connection_routes = []
        r_1 = ConnectionRouteAdditionalInfo("foo")
        r_1.setStartStructureLabel( ("TS", 1) )
        r_1.setEndStructureLabel( ("EQ", 1) )
        all_connection_routes.append(r_1)
        r_2 = ConnectionRouteAdditionalInfo("bar")
        r_2.setStartStructureLabel( ("TS", 1) )
        r_2.setEndStructureLabel( ("EQ", 2) )
        all_connection_routes.append(r_2)

        mapper= parsinghelpers.ConnectionMapper( all_connections, structure_label_to_uri_mapper, all_connection_routes)

        self.assertEqual(len( mapper.allConnectionsFor( ("TS", 1) )), 2)
        self.assertEqual(len( mapper.allConnectionsFor( ("EQ", 2) )), 1)

        self.assertEqual(mapper.structureLabelToUri( ("TS", 1) ), "urn:uuid:baz")

        self.assertEqual(len(mapper.allStructureLabels()), 3)

        self.assertEqual(mapper.connectionRouteFor( ("EQ", 2), ("TS", 1)), r_2)
        self.assertEqual(mapper.connectionRouteFor( ("TS", 1), ("EQ", 2)), r_2)
        self.assertEqual(mapper.connectionRouteFor( ("TS", 1), ("EQ", 1)), r_1)
    

        
if __name__ == '__main__':
    unittest.main()
    

