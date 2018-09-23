#!/usr/bin/env python

import os
import sys

if os.environ.has_key("PACKAGE_ROOT_DIR"):
    sys.path.insert(0,os.path.join(os.environ["PACKAGE_ROOT_DIR"],"Libraries","noarch","python", "lib", "python"))

from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens
from theochempy._theochempy import Units

from xml.dom import minidom 

def main(dalton_out, cml_out):
    tokenlist=Dalton20.tokenizeOutFile(dalton_out)

    atom_basis_set_token = getAtomsAndBasisSetsToken(tokenlist)
    geometry_token = getFinalGeometry(tokenlist)
   
    datalist = atom_basis_set_token.atomDataList()

    final_geometry = geometry_token.atomList()

    doc = minidom.parseString("<cml xmlns=\"http://www.xml-cml.org/schema\" xmlns:sb=\"http://forthescience.org/NS/mycml\"/>")
    namespace = "http://www.xml-cml.org/schema"
    molecule = doc.createElementNS(namespace,"molecule")
    doc.documentElement.appendChild(molecule)

    name = doc.createElementNS(namespace, "name")
    molecule.appendChild(name)
    text = doc.createTextNode(os.path.splitext(dalton_out)[0])
    name.appendChild(text)

    atomarray = doc.createElementNS(namespace, "atomArray")
    molecule.appendChild(atomarray)

    for id,atom_entry in enumerate(final_geometry):
        label, group, coords = atom_entry
        atomic_number = labelToAtomicNumber(label, datalist)

        atom=doc.createElementNS(namespace, "atom")
        atom.setAttribute("id", "a"+str(id+1))
        atom.setAttribute("x3", str(coords.asUnit(Units.bohr).value()[0]))
        atom.setAttribute("y3", str(coords.asUnit(Units.bohr).value()[1]))
        atom.setAttribute("z3", str(coords.asUnit(Units.bohr).value()[2]))
        atom.setAttributeNS("http://forthescience.org/NS/mycml", "sb:atomicNumber", str(atomic_number))
        label_node = doc.createElementNS(namespace, "label")
        label_node.setAttribute("value", label)
        atom.appendChild(label_node)
        atomarray.appendChild(atom)
    
    output = file(cml_out, "w")
    output.write(doc.toprettyxml())

    



def labelToAtomicNumber(find_label, datalist):
    for t in datalist:
        label, groups, atomic_number, basis_expanded, basis_contracted, basis_string = t
        if label == find_label:
            return atomic_number

    return None



def getAtomsAndBasisSetsToken(tokenlist):
    return filter(lambda x: x.__class__ == Tokens.AtomsAndBasisSetsToken, tokenlist)[0]

def getFinalGeometry(tokenlist):
    return filter(lambda x: x.__class__ == Tokens.OptimizationNextGeometryToken, tokenlist)[-1]


main(sys.argv[1], sys.argv[2])

#>>> geometries[-1].atomList()
#[('H1', '', ('0.0000002307', '-0.0431166985', '-0.0202403617')), ('H2', '', ('0.0000001751', '1.6729220095', '-3.0984614789')), ('H3', '', ('-0.0000000621', '3.9834654382', '2.2591198806')), ('H4', '', ('-0.0000004152', '6.3971763363', '-3.1312282876')), ('H5', '', ('0.0000000584', '8.7077203406', '2.2263528516')), ('H6', '', ('0.0000011485', '10.4237584759', '-0.8518686398')), ('C1', '', ('0.0000002040', '1.7527241877', '-1.0336061328')), ('C2', '', ('-0.0000000301', '3.9601114154', '0.1889860925')), ('C3', '', ('-0.0000005431', '6.4205305038', '-1.0610944968')), ('C4', '', ('-0.0000007662', '8.6279178237', '0.1614975188'))]
#>>> atoms=filter(lambda x: x.__class__ == Tokens.AtomsAndBasisSetsToken, a)
#>>> atoms
#[<TheoChemPy.FileParsers.Dalton.Tokens.AtomsAndBasisSetsToken instance at 0x2a986dd908>]
#>>> dir(atoms[0])
#['__doc__', '__init__', '__module__', '_atom_data_list', '_num_atom_types', '_num_tot_atoms', '_total_atom_data', 'atomDataList', 'match', 'numOfAtomTypes', 'totalAtomData', 'totalNumberOfAtoms']
#>>> atoms[0].atomDataList()
#[('H1', 1, 1, 7, 5, '[4s1p|2s1p]'), ('H2', 1, 1, 7, 5, '[4s1p|2s1p]'), ('H3', 1, 1, 7, 5, '[4s1p|2s1p]'), ('H4', 1, 1, 7, 5, '[4s1p|2s1p]'), ('H5', 1, 1, 7, 5, '[4s1p|2s1p]'), ('H6', 1, 1, 7, 5, '[4s1p|2s1p]'), ('C1', 1, 6, 26, 14, '[9s4p1d|3s2p1d]'), ('C2', 1, 6, 26, 14, '[9s4p1d|3s2p1d]'), ('C3', 1, 6, 26, 14, '[9s4p1d|3s2p1d]'), ('C4', 1, 6, 26, 14, '[9s4p1d|3s2p1d]')]
#>>> minidom.parseString("<cml />") 
#<xml.dom.minidom.Document instance at 0x86b98>
#>>> doc=_
#>>> doc.createElement("foo")
#<DOM Element: foo at 0x470850>
#>>> foo=_
#>>> cml=doc.firstChild  
#>>> cml
#<DOM Element: cml at 0x86e18>
#>>> cml.appendChild(foo)
#<DOM Element: foo at 0x470850>
#>>> doc.prettyXML()
#Traceback (most recent call last):
  #File "<stdin>", line 1, in ?
  #AttributeError: Document instance has no attribute 'prettyXML'
  #>>> doc.toprettyxml()
  #u'<?xml version="1.0" ?>\n<cml>\n\t<foo/>\n</cml>\n'
  #>>> print doc.toprettyxml()
  #<?xml version="1.0" ?>
  #<cml>
          #<foo/>
          #</cml>


