#!/usr/bin/env python

import sys
import gv
from glob import glob
import yaml

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

for path in glob('roles/*/meta/main.yml'):
    dependent_role = path.split('/')[1]

    add_role(dependent_role)

    with open(path, 'r') as f:
        for dependency in yaml.load(f.read())['dependencies']:
            depended_role = dependency['role']

            add_role(depended_role)
            link_roles(dependent_role, depended_role)

gv.layout(g, 'dot')
gv.render(g, 'png', 'ansible-roles.png')
