from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='wavemoldb.ordfm',
      version=version,
      description="Object-RDF mapper for wavemoldb",
      long_description="""It contains the object rdf mapper for wavemoldb""",
      classifiers=[ "License :: OSI Approved :: BSD License",
                    "Operating System :: POSIX",
                    "Programming Language :: Python",
                    "Topic :: Scientific/Engineering :: Chemistry",
                    "Topic :: Software Development :: Libraries",
                    "Topic :: Software Development :: Libraries :: Python Modules",
                    "Topic :: Utilities"
      ], 
      keywords='computational theoretical chemistry utilities wavemol',
      author='Stefano Borini',
      author_email='stefano.borini+wavemol@gmail.com',
      url='http://wavemol.org',
      license='BSD',
      packages=find_packages("lib"),
      package_dir= { '' : "lib"},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      namespace_packages = ['wavemoldb'],
      test_suite = "wavemoldb.ordfm.tests"
      )


