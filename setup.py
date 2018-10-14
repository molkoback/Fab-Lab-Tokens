from setuptools import setup

with open("README.md") as fp:
	readme = fp.read()

with open("requirements.txt") as fp:
	requirements = fp.read().splitlines()

setup(
	name="fablab-tokens",
	author="",
	author_email="",
	url="https://github.com/molkoback/Fab-Lab-Tokens",
	packages=["tokens", "fetcher"],
	version="0.1.0",
	license="MIT",
	description="Fab Lab token system software project",
	long_description=readme,
	install_requires=requirements,
	classifiers=[]
)
