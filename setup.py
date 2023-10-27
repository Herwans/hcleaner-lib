from setuptools import find_packages, setup

setup(
    name='hcleanerlib',
    packages=find_packages(),
    setup_requires=['Pillow'],
    version='2.0.0',
    description='The library for the HCleaner GUI and HCleaner CLI projects',
    author="Herwans Harvel",
    license='MIT'
)