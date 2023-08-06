from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A basic menu generator'


# Setting up
setup(
    name="menuer",
    version=VERSION,
    author="Ben Wilcken",
    author_email="goast75@web.de",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['termcolor', 'pyfiglet'],
    keywords=['python', 'menu', 'generator', 'terminal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
