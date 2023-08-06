import os
from setuptools import setup, find_packages

VERSION = '1.1.4'
DESCRIPTION = 'Sellix.IO API wrapper written in Python.'
LONG_DESRIPTION = 'Documentation can be found on the Github repo.'

# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="sellix-py-api-wrapper",
    version=VERSION,
    author="Mlchael",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    # long_description=read('README.md'),
    long_description=LONG_DESRIPTION,
    install_requires=['requests'],
    keywords=['python3', 'sellix', 'sellix.io', 'api', 'api wrapper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
