#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from os.path import join
import gv
from glob import glob
import yaml

def parse_args(args):
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

args = parse_args(sys.argv[1:])

class GraphBuilder:
    def __init__(self):
        self.graph = gv.digraph('roles')
        self._role_nodes = {}

    def add_role(self, role):
        if role not in self._role_nodes:
            self._role_nodes[role] = gv.node(self.graph, role)

    def link_roles(self, dependent, depended):
        gv.edge(
            self._role_nodes[dependent_role],
            self._role_nodes[depended_role]
        )

builder = GraphBuilder()

for roles_dir in args.roles_dirs:
    for path in glob(join(roles_dir, '*/meta/main.yml')):
        dependent_role = path.split('/')[-3]

        builder.add_role(dependent_role)

        with open(path, 'r') as f:
            for dependency in yaml.load(f.read())['dependencies']:
                depended_role = dependency['role']

                builder.add_role(depended_role)
                builder.link_roles(dependent_role, depended_role)

gv.layout(builder.graph, 'dot')
gv.render(builder.graph, args.format, args.output)
