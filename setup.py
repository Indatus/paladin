# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
import os
from setuptools import setup

with open('description.rst', 'rb') as f:
	long_descr = f.read().decode('utf-8')

setup(
	name = 'r2d2',
	packages = ['r2d2'],
	entry_points = {
		'console_scripts': ['r2d2 = r2d2.r2d2:main']
	},
	version	= '0.3.6',
	description = "Android Dependency Manager for libraries that aren't packaged as .jar or .aar",
	long_description = long_descr,
	author = "Jonathon Staff",
	author_email = "jon@isprime-design.com",
	url = "http://jonathonstaff.com"
	)
