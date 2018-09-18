#!/usr/bin/env python
# @author Stefano Borini 

from distutils.core import setup

setup(name='TheoChemPy',
      version='1.0.0',
      author="Stefano Borini",
      author_email="moc.liamg@ypmehcoeht+inirob.onafets",
      maintainer="Stefano Borini",
      maintainer_email="moc.liamg@ypmehcoeht+inirob.onafets",
      description="A library for Theoretical chemists",
      packages=['TheoChemPy', "TheoChemPy.FileParsers",  "TheoChemPy.FileParsers.Dalton","TheoChemPy.Geometry", "TheoChemPy.IO", "TheoChemPy.Math", "TheoChemPy.Net", "TheoChemPy.Utils"    ],
      package_dir={'TheoChemPy' : 'TheoChemPy'},
      scripts=['utils/zmat2input']
      )
