""" Setuptools/Distribute script."""

from setuptools import setup, find_packages


version = "0.1"
long_description = open("README").read() + "\n" + open("CHANGES").read()
description = "Framework for reusable and composable UI with repoze.bfg."
requires = []


setup(name="contentlet",
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: BFG",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords="web wsgi bfg ui",
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      url="http://packages.python.org/contentlet",
      license="BSD",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      test_suite="contentlet.tests",
      )
