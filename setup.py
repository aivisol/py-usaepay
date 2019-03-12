#!/usr/bin/env python

#
# setup script
#

from distutils.core import setup

# install
dist = setup(
	name="usaepay",
	version="0.0.1-CURRENT",
	description="Python Usaepay",
	author="DataTechLabs",
	author_email="info@datatechlabs.com",
	url="https://datatechlabs.com",
	packages=["usaepay"]
)
