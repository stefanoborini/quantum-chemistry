from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='wavemol.math',
      version=version,
      description="Math/Geometry utility classes for wavemol project",
      long_description="""\
Math/Geometry utility classes for wavemol project""",
      classifiers=[ "License :: OSI Approved :: BSD License",
                    "Operating System :: POSIX",
                    "Programming Language :: Python",
                    "Topic :: Scientific/Engineering :: Mathematics",
                    "Topic :: Software Development :: Libraries",
                    "Topic :: Software Development :: Libraries :: Python Modules",
                    "Topic :: Utilities"
      ], 
      keywords='wavemol math geometry computational chemistry quantum',
      author='Stefano Borini',
      author_email='stefano.borini+wavemol@gmail.com',
      url='http://wavemol.org',
      license='BSD',
      packages=find_packages("lib", exclude=['ez_setup', 'examples', 'tests']),
      package_dir= { '' : "lib"},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "wavemol.core >= 0.1.0dev"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      namespace_packages = ['wavemol'],
      test_suite = "wavemol.math.tests"
      )







