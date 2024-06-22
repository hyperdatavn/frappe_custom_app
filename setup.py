from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_custom_app/__init__.py
from frappe_custom_app import __version__ as version

setup(
	name="frappe_custom_app",
	version=version,
	description="custom app",
	author="duongtk",
	author_email="khanhduongtram@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
