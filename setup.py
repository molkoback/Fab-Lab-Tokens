from setuptools import setup

with open("README.md") as fp:
	readme = fp.read()

with open("requirements.txt") as fp:
	requirements = fp.read().splitlines()

setup(
	name="fablab-tokens",
	author="Eero Molkoselkä, Jonada Ferracaku",
	author_email="eero.molkoselka@gmail.com, jonada.ferracaku@gmail.com",
	url="https://github.com/molkoback/Fab-Lab-Tokens",
	packages=["tokens", "fetcher"],
	package_data={"tokens": ["sol/bank.sol"]},
	include_package_data=True,
	version="0.1.0",
	license="MIT",
	description="Fab Lab token system software project",
	long_description=readme,
	install_requires=requirements,
	classifiers=[
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Topic :: Internet"
	]
)
