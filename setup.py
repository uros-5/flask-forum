import os
from setuptools import setup

setup(
	name="my_app",
	version="1.0",
	author="Uros Mrkobrada",
	author_email="uros.mrkobrada99@gmail.com",
	description="uefa_comps application",
	packages=["my_app"],
	platforms="any",
	install_requires= [
		"flask",

	],
	classifiers = [
		"Development Status:: 4 - Beta",
		"Environment :: Web Environment",
		"Intended Audince :: Developers",
		"Licence :: OSI Approved :: GNU General Public Licence v3",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Topic :: Internet :: WWW/HTTP :: Dynamic Content",
		"Topic :: Software Development :: Libraries :: Pyton Modules"
	]
)