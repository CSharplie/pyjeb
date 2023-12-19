from setuptools import setup, find_packages

with open('../README.md') as f:
    long_description = "".join(f.readlines())

# replace relative link by absolute github link
long_description = long_description.replace("(/", "(https://github.com/CSharplie/pyjeb/blob/main/")
print(long_description)


setup (
    name = "pyjeb",
    version = "0.1.8",
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