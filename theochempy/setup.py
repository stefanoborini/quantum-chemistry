#!/usr/bin/env python
# @author Stefano Borini 

from distutils.core import setup

setup(name='theochempy',
      version='0.15.0',
      author="Stefano Borini",
      author_email="moc.liamg@ypmehcoeht+inirob.onafets",
      maintainer="Stefano Borini",
      maintainer_email="moc.liamg@ypmehcoeht+inirob.onafets",
      description="A library for theoretical chemists",
      packages=[    'theochempy', 
                    "theochempy._theochempy",
                    "theochempy._theochempy.Chemistry",
                    "theochempy._theochempy.Chemistry.PeriodicTable",
                    "theochempy._theochempy.FileParsers",  
                    "theochempy._theochempy.FileParsers.Dalton20",
                    "theochempy._theochempy.FileParsers.GRRM",
                    "theochempy._theochempy.FileParsers.GRRMInput",
                    "theochempy._theochempy.FileParsers.Molcas",
                    "theochempy._theochempy.FileParsers.ZMatrix",
                    "theochempy._theochempy.Geometry", 
                    "theochempy._theochempy.IO", 
                    "theochempy._theochempy.Math", 
                    "theochempy._theochempy.Net", 
                    "theochempy._theochempy.InputGenerators", 
                    "theochempy._theochempy.InputGenerators.Dalton20",
                    "theochempy._theochempy.Engines",
                    "theochempy._theochempy.Molecules",
                    "theochempy._theochempy.Databases",
                    "theochempy._theochempy.Databases.Simple",
                    "theochempy._theochempy.GraphDataModel",
                    ],
      package_dir={'theochempy' : 'theochempy'},
      )

