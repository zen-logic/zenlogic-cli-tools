import os, argparse
from fh_cli import CLI

if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog='fh',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
Zen Logic file hunter
Track, manage and consolidate files across multiple locations, external storage (such as USB drives) or network mounts.
        '''
    )
    
    parser.add_argument(
        '-o', '--output',
        help='output format (default is table)',
        nargs='?', default='table',
        choices=['json', 'table'])
    
    parser.add_argument(
        '-f', '--fields',
        help='comma separated list of fields to output (default is all fields)',
        nargs='?')
    
    parser.add_argument(
        '-d', '--database',
        help='database file to use (default is $HOME/.zenlogic/fh.db)',
        nargs='?')
     
    sub = parser.add_subparsers(
        description='valid subcommands',
        dest='command')
     
    # create the command parsers
    cmd = sub.add_parser(
        'match',
        help='match file by hash')
    cmd.add_argument(
        'filename',
        help='file to match')
     
    cmd = sub.add_parser(
        'find',
        help='find item (file, folder, path, hash, ext)')
    cmd.add_argument(
        'type',
        help='item type to find',
        choices=['file', 'folder', 'path', 'hash', 'ext'])
    cmd.add_argument(
        'item',
        help='item to find')
    cmd.add_argument(
        '-e', '--end',
        action='store_true',
        help='match to end of path')
    cmd.add_argument(
        '-s', '--start',
        action='store_true',
        help='match to start of path')
     
    cmd = sub.add_parser(
        'hierarchy',
        help='list folder hierarchy from folder id')
    cmd.add_argument(
        'id',
        help='folder id to show')
     
    cmd = sub.add_parser(
        'compare',
        help='find differences items in folder structure')
    cmd.add_argument('a', help='first folder id')
    cmd.add_argument('b', help='second folder id')

    cmd.add_argument(
        'operation',
        default='difference',
        choices=['a-not-b', 'b-not-a', 'difference', 'both', 'union'],
        help='return items in either a or b but not in both')
     
    cmd = sub.add_parser(
        'list',
        help='list items in folder id')
    cmd.add_argument(
        'item',
        help="folder id")

    cmd = sub.add_parser(
        'roots',
        help='list storage roots')

    cmd = sub.add_parser(
        'scan',
        help='scan folder/drive and create a storage root')
    cmd.add_argument(
        'name',
        help="name for the new storage root")
    cmd.add_argument(
        'path',
        help="path to the root of the folder or drive")

    cmd = sub.add_parser(
        'get',
        help='get item by id (file, folder)')
    cmd.add_argument(
        'type',
        help='item type to get',
        choices=['file', 'folder'])
    cmd.add_argument(
        'id',
        help='item id')

    
    args = parser.parse_args()
    
    if args.command:
        cli = CLI(args)
    else:
        parser.print_help()
