from setuptools import setup, find_packages
import glob
import os
import sys

from taca import __version__
from io import open

try:
    with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

try:
    with open("dependency_links.txt", "r") as f:
        dependency_links = [x.strip() for x in f.readlines()]
except IOError:
    dependency_links = []


setup(name='taca',
    version=__version__,
    description="Tool for the Automation of Cleanup and Analyses",
    long_description='This package contains a set of functionalities that are '
                   'useful in the day-to-day tasks of bioinformatitians in '
                   'National Genomics Infrastructure in Stockholm, Sweden.',
    keywords='bioinformatics',
    author='NGI-stockholm',
    author_email='ngi_pipeline_operators@scilifelab.se',
    url='http://taca.readthedocs.org/en/latest/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    scripts=glob.glob('scripts/*.py'),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['taca = taca.cli:cli'],
        'taca.subcommands': [
            'cleanup = taca.cleanup.cli:cleanup',
            'analysis = taca.analysis.cli:analysis',
            'bioinfo_deliveries = taca.utils.cli:bioinfo_deliveries',
            'server_status = taca.server_status.cli:server_status',
            'backup = taca.backup.cli:backup',
            'create_env = taca.testing.cli:uppmax_env'
        ]
    },
    install_requires=install_requires,
    dependency_links=dependency_links
)
