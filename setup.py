""" Setuptools/Distribute script."""

from setuptools import setup, find_packages


version = "0.1"
long_description = open("README").read() + "\n" + open("CHANGES").read()
description = "Framework for reusable and composable UI with repoze.bfg."
requires = [
    "repoze.bfg",
    ]


setup(name="contentlet",
      version=version,
      description=description,
      long_description=long_description,
      keywords="web wsgi bfg ui",
      author="Andrey Popp",
      author_email="8mayday@gmail.com",
      url="http://braintrace.ru",
      license="BSD",
      packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      test_suite="contentlet.tests",
      )
