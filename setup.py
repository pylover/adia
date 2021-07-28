import re

from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'adia', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    'easycli',
]


setup(
    name='adia',
    version=package_version,
    packages=find_packages(exclude=['tests']),
    install_requires=dependencies,
    license='MIT',
    entry_points={
        'console_scripts': [
            'adia = adiacli:ADia.quickstart',
        ]
    },

    description='Language for ASCII diagrams.',
    url='http://github.com/pylover/adia',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Text Processing',
    ]
)
