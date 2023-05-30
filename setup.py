import re

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

version = "1.0.0"

setup(
    name="amendements2json",
    version=version,
    description="Extract amendments from European Parliament docx files",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Sebastien Campion",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=open("requirements.txt").read().splitlines(),
)
