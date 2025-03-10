import os, argparse
from core.cli_fh import CLI

if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog='zfh',
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
        dest='command',
        metavar='')
     
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
        help='match to end')
    cmd.add_argument(
        '-i', '--ignorecase',
        action='store_true',
        help='ignore case')
    cmd.add_argument(
        '-s', '--start',
        action='store_true',
        help='match to start')
    cmd.add_argument(
        '-p', '--partial',
        action='store_true',
        help='partial match')
     
    cmd = sub.add_parser(
        'hierarchy',
        help='list folder hierarchy from folder id')
    cmd.add_argument(
        'id',
        help='folder id to show')
     
    cmd = sub.add_parser(
        'compare',
        help='find differences in folder structure')
    cmd.add_argument(
        'type',
        help='comparison type (default is folders)',
        default='folders',
        choices=['folders', 'files'])
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
        'items',
        help='list files and folders in folder id')
    cmd.add_argument(
        'item',
        help="folder id")

    cmd = sub.add_parser(
        'roots',
        help='list storage roots')

    cmd = sub.add_parser(
        'root',
        help='list storage root contents')
    cmd.add_argument(
        'item',
        help="root id")

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

    cmd = sub.add_parser(
        'tree',
        help='folder tree')
    cmd.add_argument(
        'folder',
        help='folder id to retrieve')
    cmd.add_argument(
        '-f', '--files',
        action='store_true',
        help='show files')
 
    
    args = parser.parse_args()
    
    if args.command:
        cli = CLI(args)
    else:
        parser.print_help()
