from ansiblerolesgraph import __version__, __author__
from setuptools import setup

setup(
    name='ansible-roles-graph',
    version=__version__,

    description='Generate a graph of Ansible role dependencies.',
    url = 'https://github.com/sebn/ansible-roles-graph',

    author=__author__,
    author_email='sebastien@nicouleaud.net',

    license='GPLv3+',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Documentation',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    keywords='ansible roles graph',

    packages=['ansiblerolesgraph'],

    install_requires=[
        'PyYAML',
    ],

    entry_points={
        'console_scripts': [
            'ansible-roles-graph=ansiblerolesgraph:main',
        ],
    },
)
