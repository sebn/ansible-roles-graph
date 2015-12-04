#!/usr/bin/env python

from argparse import ArgumentParser
from os.path import join
import gv
from glob import glob
import yaml

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

args = p.parse_args()
g = gv.digraph('roles')
role_nodes = {}

def add_role(role):
    if role not in role_nodes:
        role_nodes[role] = gv.node(g, role)

def link_roles(dependent, depended):
    gv.edge(
        role_nodes[dependent_role],
        role_nodes[depended_role]
    )

for roles_dir in args.roles_dirs:
    for path in glob(join(roles_dir, '*/meta/main.yml')):
        dependent_role = path.split('/')[-3]

        add_role(dependent_role)

        with open(path, 'r') as f:
            for dependency in yaml.load(f.read())['dependencies']:
                depended_role = dependency['role']

                add_role(depended_role)
                link_roles(dependent_role, depended_role)

gv.layout(g, 'dot')
gv.render(g, args.format, args.output)
