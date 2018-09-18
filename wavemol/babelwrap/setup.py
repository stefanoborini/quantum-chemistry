from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='babelwrap',
      version=version,
      description="Keeps openbabel/pybel GPL code in the doghouse",
      long_description="""\
This module contains simple utility programs wrapping openbabel/pybel functionalities so that wavemol projects can take advantage of their functionalities without being forced to use GPL""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='openbabel wrap',
      author='Stefano Borini',
      author_email='stefano.borini+babelwrap@gmail.com',
      url='http://wavemol.org',
      license='GPL v2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points = {
               'console_scripts': [
                     'bwrap_xyz2inchi = babelwrap.executables:bwrap_xyz2inchi',
                     'bwrap_xyz2smiles = babelwrap.executables:bwrap_xyz2smiles',
                     'bwrap_xyz2molweight = babelwrap.executables:bwrap_xyz2molweight',
                   ],
      }

      ,
      )
