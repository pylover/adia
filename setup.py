import re

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'dial', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    'easycli',
]


setup(
    name='dial',
    version=package_version,
    packages=find_packages(exclude=['tests']),
    install_requires=dependencies,
    license='MIT',
    entry_points={
        'console_scripts': [
            'dial = dialcli:Dial.quickstart',
        ]
    },
)
