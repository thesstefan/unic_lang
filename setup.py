from setuptools import setup, find_namespace_packages

setup(
    name='unic',
    version='1.0',
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': ['unic = unic.cli.cli:main']
    })
