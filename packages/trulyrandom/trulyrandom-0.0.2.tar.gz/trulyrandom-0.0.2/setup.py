from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.2'
DESCRIPTION = 'random.org API Implementation in Python'

# Setting up
setup(
    name="trulyrandom",
    version=VERSION,
    author="Envoy-VC (Vedant Chainani)",
    author_email="vedantchainani1084@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'random', 'api', 'json'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)