from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='wavemol.core',
      version=version,
      description="Core functionality for wavemol",
      long_description="""This package is part of the wavemol set of tools for computational chemists.
It contains core functionality useful as a basis for the other modules.
""",
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
          "quantities >= 0.6.0"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      namespace_packages = ['wavemol'],
      test_suite = "wavemol.core.tests"
      )


