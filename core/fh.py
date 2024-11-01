from fh_cli import CLI

if __name__ == '__main__':
    import argparse
    
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='fh')
    parser.add_argument(
        '-o', '--output',
        help='output format',
        nargs='?', default='json',
        choices=['json', 'fields'])
    parser.add_argument(
        '-f', '--fields',
        help='comma separated list of fields to output',
        nargs='?')
    parser.add_argument(
        '-d', '--database',
        help='database file to use',
        nargs='?')
     
    sub = parser.add_subparsers(
        description='valid subcommands',
        dest='command')
     
    # create the command parsers
    p = sub.add_parser(
        'match',
        help='match file by hash')
    p.add_argument(
        'filename',
        help='file to match')
     
    p = sub.add_parser(
        'find',
        help='find item (file, folder, path, hash, ext)')
    p.add_argument(
        'type',
        help='item type to find',
        choices=['file', 'folder', 'path', 'hash', 'ext'])
    p.add_argument(
        'item',
        help='item to find')
    p.add_argument(
        '-e', '--end',
        action='store_true',
        help='match to end of path')
    p.add_argument(
        '-s', '--start',
        action='store_true',
        help='match to start of path')
     
    p = sub.add_parser(
        'hierarchy',
        help='show folder hierarchy')
    p.add_argument(
        'id',
        help='folder id to show')
     
    p = sub.add_parser(
        'diff',
        help='find differences items in folder structure')
    p.add_argument('a', help='first folder id')
    p.add_argument('b', help='second folder id')
    p.add_argument(
        '-a', '--all',
        action='store_true',
        help='return items in either a or b but not in both')
     
    p = sub.add_parser(
        'list',
        help='list files in folder or storage roots')
    p.add_argument(
        'item',
        help="folder id or 'roots'")

    p = sub.add_parser(
        'scan',
        help='scan folder/drive and create a storage root')
    p.add_argument(
        'name',
        help="name for the new storage root")
    p.add_argument(
        'path',
        help="path to the root of the folder or drive")

    p = sub.add_parser(
        'merge',
        help='combine 2 folder structures')
    p.add_argument('a', help='first folder id')
    p.add_argument('b', help='second folder id')


    p = sub.add_parser(
        'get',
        help='get item by id (file, folder)')
    p.add_argument(
        'type',
        help='item type to get',
        choices=['file', 'folder'])
    p.add_argument(
        'id',
        help='item id')

    
    args = parser.parse_args()
    
    if args.command:
        cli = CLI(args)
    else:
        parser.print_help()
