# standard setup.py file

from setuptools import setup, find_packages

setup(
    name='Artifex-Platformer',
    version='0.1',
    description="A platformer game called 'Artifex' where the player must navigate through a series of trecherous levels, collect and combine spirits, to save the love of their life.",
    license='MIT',
    author='Peter Zhang',
    install_requires=[
        "pygame-ce==2.4.1",
        "moderngl==5.10.0",
        "numba==0.59.1",
    ]
) 