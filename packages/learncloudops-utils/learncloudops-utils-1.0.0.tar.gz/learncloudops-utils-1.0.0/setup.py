import pathlib
from setuptools import setup, find_packages

# the directory containing this file
HERE = pathlib.Path(__file__).parent

# the test of the README file
README = (HERE / "README.md").read_text()

# this call to setup() does all the work
setup(
    name="learncloudops-utils",
    version="1.0.0",
    description="Utilities for building Python apps in AWS",
    long_description=README,
    long_descritpion_content_type="text/markdown",
    url="https://github.com/learncloudops/awsutils",
    author="learncloudops.com",
    author_email="matt@learncloudops.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",        
    ],
    packages= find_packages(exclude=("tests")),
    include_package_data=True,
    install_requires=["boto3"]



)