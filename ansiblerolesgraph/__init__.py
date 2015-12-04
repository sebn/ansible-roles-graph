#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from os.path import join
import gv
from glob import glob
import yaml

__version__ = '0.1.0'
__author__  = 'Sebastien Nicouleaud'

def parse_args(args):
    """Parse the command-line arguments and return a config object.

        >>> config = parse_args(['-o', 'schema.jpg',
        ...                      '-f', 'jpg',
        ...                      'roles/',
        ...                      '../other/roles'])
        >>> config.output
        'schema.jpg'
        >>> config.format
        'jpg'
        >>> config.roles_dirs
        ['roles/', '../other/roles']
    """
    p = ArgumentParser(description='Generate a picture of ansible roles graph.')

    p.add_argument('roles_dirs',
                   metavar='ROLES_DIR',
                   type=str,
                   nargs='+',
                   default='./roles/',
                   help='a directory containing ansible roles')

    p.add_argument('-o', '--output',
                   type=str,
                   default='./ansible-roles.png',
                   help='the output file')

    p.add_argument('-f', '--format',
                   type=str,
                   default='png')

    return p.parse_args(args)

class GraphBuilder:
    def __init__(self):
        self.graph = gv.digraph('roles')
        self._role_nodes = {}

    def add_role(self, role):
        if role not in self._role_nodes:
            self._role_nodes[role] = gv.node(self.graph, role)

    def link_roles(self, dependent_role, depended_role):
        gv.edge(
            self._role_nodes[dependent_role],
            self._role_nodes[depended_role]
        )

def parse_roles(roles_dirs, builder=GraphBuilder()):
    for roles_dir in roles_dirs:
        for path in glob(join(roles_dir, '*/meta/main.yml')):
            dependent_role = path.split('/')[-3]

            builder.add_role(dependent_role)

            with open(path, 'r') as f:
                for dependency in yaml.load(f.read())['dependencies']:
                    depended_role = dependency['role']

                    builder.add_role(depended_role)
                    builder.link_roles(dependent_role, depended_role)

    return builder.graph

def render_graph(graph, config):
    gv.layout(graph, 'dot')
    gv.render(graph, config.format, config.output)

def main():
    config = parse_args(sys.argv[1:])
    graph = parse_roles(config.roles_dirs)
    render_graph(graph, config)

if __name__ == '__main__':
    main()
