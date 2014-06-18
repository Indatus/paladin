# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
import os
from setuptools import setup

with open('description.rst', 'rb') as f:
	long_descr = f.read().decode('utf-8')

setup(
	name = 'paladin',
	packages = ['paladin'],
	entry_points = {
		'console_scripts': ['paladin = paladin.paladin:main']
	},
	version	= '0.5.2',
	description = "Android Dependency Manager for libraries that aren't packaged as .jar or .aar - Paladin fells your dependencies like a boss.",
	long_description = long_descr,
	author = "Jonathon Staff",
	author_email = "jon@nplexity.com",
	url = "http://jonathonstaff.com/paladin"
	)
