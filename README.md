# ansible-roles-graph

Generate a graph of Ansible role dependencies.

## Install

    pip install ansible-roles-graph

## Usage

Quite simply:

    ansible-roles-graph

Will look for roles in the `./roles/` directory, and generate an `./ansible-roles.png` file.

The command also accepts multiple role directories and various options:

    ansible-roles-graph -o schema.png -f png roles/ ../other/roles

See `ansible-roles-graph --help` for more info.

## Output

![PNG example](./example.png)

## License

[GNU GPLv3](https://www.gnu.org/licenses/gpl.html)
