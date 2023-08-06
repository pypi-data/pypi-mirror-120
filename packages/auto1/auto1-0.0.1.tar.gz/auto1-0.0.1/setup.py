
from sys import version
from setuptools import setup, find_packages
from os import path, environ


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


project_name = 'auto1'
project_description = 'AUTO1 ETL Pipeline'
project_author_name = 'Abdul Salam'
project_author_email = 'salamsol96@gmail.com'

environ['APP_ID'] = project_name


setup(
    name=project_name,
    version='0.0.1',
    description=project_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=project_author_name,
    author_email=project_author_email,
    packages=find_packages(),
    
    # Specify which python version you support, 
    # pip install will check this and refuse to
    # install the project if the version does not match.

    python_requires='>=3.7, <4'
)