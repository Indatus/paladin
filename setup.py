# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

with open('description.rst', 'rb') as f:
	long_descr = f.read().decode('utf-8')

setup(
	name = 'adm',
	packages = ['adm'],
	entry_points = {
		'console_scripts': ['adm = adm.adm:main']
	},
	version	= '0.1.0',
	description = "Android Dependency Manager for libraries that aren't packaged as .jar or .aar",
	long_description = long_descr,
	author = "Jonathon Staff",
	author_email = "jon@isprime-design.com",
	url = "http://jonathonstaff.com"
	)
