"""Setup PyPi module"""
# pylint: disable=C0103

from setuptools import setup, find_packages

with open("../README.md", encoding="UTF-8") as f:
    long_description = "".join(f.readlines())

# replace relative link by absolute github link
long_description = long_description.replace("(/", "(https://github.com/CSharplie/pyjeb/blob/main/")

setup (
    name = "pyjeb",
    version = "0.1.10",
    description="A lightweight library to check and variabilize your configuration files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CSharplie/pyjeb/",
    project_urls={
        "Bug Tracker": "https://github.com/CSharplie/pyjeb/issues",
        "CI": "https://github.com/CSharplie/pyjeb/actions",
        "Documentation": "https://github.com/CSharplie/pyjeb",
        "Source Code": "https://github.com/CSharplie/pyjeb",
    },
    download_url="https://pypi.org/project/pyjeb/",
    platforms="Any",
    python_requires=">=3.6",
    license= "Apache License 2.0",
    packages = find_packages(),
)
