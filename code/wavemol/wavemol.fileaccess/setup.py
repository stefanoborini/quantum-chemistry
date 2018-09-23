from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='wavemol.fileaccess',
      version=version,
      description="Provides functionality for read, write and modify useful file formats",
      long_description="""\
Provides functionality for read, write and modify useful file formats""",
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
          "wavemol.core >= 0.1.0"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      namespace_packages = ['wavemol'],
      test_suite = "wavemol.fileaccess.tests"
      )

