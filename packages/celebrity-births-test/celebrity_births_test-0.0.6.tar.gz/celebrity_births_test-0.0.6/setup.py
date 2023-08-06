from setuptools import setup
from setuptools import find_packages

setup(
    name='celebrity_births_test',
    version='0.0.6',
    description='Mock package that allows you to find celebrity by date of birth',
    # long_description=,
    url='https://github.com/IvanYingX/project_structure_pypi.git',
    author='Ivan Ying',
    license='MIT',
    packages=['celebrity_births'],
    install_requires=['requests==2.26.0', 'beautifulsoup4'],
)