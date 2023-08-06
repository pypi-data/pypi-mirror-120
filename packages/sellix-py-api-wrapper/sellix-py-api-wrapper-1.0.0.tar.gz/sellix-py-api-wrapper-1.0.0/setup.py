from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Sellix.IO API wrapper written in Python.'

setup(
    name="sellix-py-api-wrapper",
    version=VERSION,
    author="Mlchael",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['json', 'requests'],
    keywords=['python3', 'sellix', 'sellix.io', 'api', 'api wrapper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
