import re

from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

version = "1.0.3"

requirements = open("requirements.txt").read().splitlines()

setup(
    name="europarl_amendment_extract",
    version=version,
    description="Extract amendments from European Parliament docx files",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Sebastien Campion",
    license="MIT",
    packages=['ep_amendment_extract'],
    install_requires=requirements,
)
