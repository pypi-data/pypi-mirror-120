#!/usr/bin/env python
#******************************************************************************
# Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
#******************************************************************************
""" Setup script for the utmpx module. """

import os as _os, os.path as _path
import subprocess as _subprocess
from setuptools import setup as _setup, Extension as _Extension

version = "0.4.1"

# ---
# Find the sources.
# ---

def find_ext(dirpath, *extensions):
	""" Find with extensions. """

	def _find_iter():
		for dpath, _, fnames in _os.walk(dirpath):
			for fname in fnames:
				if fname.split('.')[-1] in extensions:
					yield _path.join(dpath, fname)

	return list(_find_iter())

srcdir = "src"

src = find_ext(srcdir, "c")
hdr = find_ext(srcdir, "h")

# ---
# Run the setup script.
# ---

_setup(
	name = 'pyutmpx',
	version = version,
	license = 'MIT',

	url = 'https://pyutmpx.touhey.pro/',
	description = 'user accounting databases reader on UNIX-like systems',
	long_description = open('README.rst', 'r').read(),
	keywords = 'utmp, utmpx, btmp, btmpx, wtmp, wtmpx, lastlog',
	platforms = ['linux', 'openbsd6'],
	classifiers = [
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Developers',
		'Topic :: System :: Systems Administration'],

	author = 'Thomas Touhey',
	author_email = 'thomas@touhey.fr',

	ext_modules = [_Extension("pyutmpx", src,
		include_dirs = [], library_dirs = [], libraries = [],
		language = 'c', depends = hdr,
		define_macros = [('PYUTMPX_VERSION', f'"{version}"')])],

	zip_safe = False,
	include_package_data = True,
	package_data = {
		'*': ['*.txt', '*.rst']
	}
)

# End of file.
