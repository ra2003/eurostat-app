from setuptools import setup, find_packages
import sys, os

__version__ = '0.1'

setup(
	name='eurostat',
	version=__version__,
	description='Eurostat browser and data proxy',
	long_description='',
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Open Knowledge Foundation',
	author_email='rufus.pollock@okfn.org',
	url='http://eurostat.okfn.org/',
	license='mit',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
)
