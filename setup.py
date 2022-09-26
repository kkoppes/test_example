"""pylantir setup script."""

import os
import sys
from setuptools import setup, find_packages

# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

# Get the version from the VERSION file
with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    version = f.read().strip()

# Get the requirements from the environment.yml file
with open(os.path.join(os.getcwd(), 'environment.yml')) as f:
    requirements = f.read().split(' ')[2:]
    #remove empty strings and "" and - and newlines
    requirements = [x for x in requirements if x != '' and x != '"' and x != '-' and x != '\n']
    #remove newline characters
    requirements = [x.replace('\n', '') for x in requirements]
    print(requirements)

setup(
    name='pylantir',
    version=version,
    description='Python package for KI Engineering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='git.de.pa.corp:8443/projects/ENG/repos/pylantir/browse',
    author='Kristiaan Koppes',
    author_email='kristiaan.koppes@airbus.com',
    license='Internal',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='python pylantir',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.10',
    project_urls={
        'Bug Reports': 'git.de.pa.corp:8443/projects/ENG/repos/pylantir/browse',
        'Source': 'git.de.pa.corp:8443/projects/ENG/repos/pylantir/browse',
    },
)

# End of file







