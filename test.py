import argparse

# create the top-level parser
parser = argparse.ArgumentParser(prog='fh')
parser.add_argument('-o', '--output',
                    help='output format',
                    nargs='?', default='json',
                    choices=['json', 'fields'])
parser.add_argument('-f', '--fields',
                    help='comma separated list of fields to output',
                    nargs='?')

sub = parser.add_subparsers(description='valid subcommands',
                            dest='command')

# create the command parsers
p1 = sub.add_parser('match', help='match file by hash')
p1.add_argument('filename', help='file to match')

p2 = sub.add_parser('find',
                    help='find item (file, folder, path, hash)')
p2.add_argument('type', help='item type to find',
                choices=['file', 'folder', 'path', 'hash'])
p2.add_argument('item', help='item to find')
p2.add_argument('-e', '--end', action='store_true',
                help='match to end of path')
p2.add_argument('-s', '--start', action='store_true',
                help='match to start of path')

p3 = sub.add_parser('hierarchy', help='show folder hierarchy')
p3.add_argument('id', help='folder id to show')

p4 = sub.add_parser('diff',
                    help='find items in folder a, not in folder b)')
p4.add_argument('a', help='first folder id')
p4.add_argument('b', help='second folder id')
p4.add_argument('-a', '--all', action='store_true',
                help='return items in either a or b but not in both')

p5 = sub.add_parser('list',
                    help='list files in folder or storage roots')
p5.add_argument('item', help="folder id or 'roots'")

args = parser.parse_args()

print(args)


