# Used to set the project folder to local package

from setuptools import setup, find_packages

setup(
    name="us_visa",
    version="0.0.0",
    author="HKT",
    author_email="ktung1112006@gmail.com",
    packages=find_packages() # Find all the folder with __init__.py and push them in local package
)