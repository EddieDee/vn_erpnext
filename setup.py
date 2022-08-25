from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in berenice/__init__.py
from berenice import __version__ as version

setup(
	name="berenice",
	version=version,
	description="Berenice app",
	author="Verynice SRL",
	author_email="info@verynicesrl",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
