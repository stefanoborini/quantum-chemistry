#import ez_setup
#ez_setup.use_setuptools()
from setuptools import setup, find_packages
import sys, os

version = '0.2.0'
setup(name='wavemol.parsers',
      version=version,
      description="A set of parsers for quantum chemistry files",
      long_description="""A set of parsers for quantum chemistry files""",
      classifiers=[ "License :: OSI Approved :: BSD License",
                    "Operating System :: POSIX",
                    "Programming Language :: Python",
                    "Topic :: Scientific/Engineering :: Chemistry",
                    "Topic :: Software Development :: Libraries",
                    "Topic :: Software Development :: Libraries :: Python Modules",
                    "Topic :: Utilities"
      ], 
      keywords='theoretical chemistry computational library',
      author='Stefano Borini',
      author_email='stefano.borini+wavemol@gmail.com',
      url='http://wavemol.org',
      license='BSD',
      packages=find_packages("lib", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      package_dir={"": "lib"},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          "wavemol.core >= 0.1.0dev",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      namespace_packages = ['wavemol'],
      test_suite = "wavemol.parsers.tests"
      )
