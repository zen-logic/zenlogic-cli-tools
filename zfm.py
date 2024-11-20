import os, argparse
from core.cli_fm import CLI

if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog='zfm',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'''
Zen Logic file manager
        '''
    )
    
    parser.add_argument(
        '-d', '--database',
        help='database file to use (default is $HOME/.zenlogic/fh.db)',
        nargs='?')

    parser.add_argument(
        '-r', '--root',
        help='override storage root path',
        nargs='?')

    parser.add_argument(
        '-m', '--mount',
        help='mount point for storage folder',
        nargs='?')
    
    sub = parser.add_subparsers(
        description='valid subcommands',
        dest='command',
        metavar='')
     
    # create the command parsers
    cmd = sub.add_parser(
        'copy',
        help='copy file by id')
    cmd.add_argument(
        'id',
        help='file id to retrieve')
    cmd.add_argument(
        'dst',
        help='where to copy the file')

    cmd = sub.add_parser(
        'merge',
        help='merge folders')
    cmd.add_argument(
        '-d', '--dst',
        required=True,
        help='where to copy the file')
    cmd.add_argument(
        '-r', '--recurse',
        action='store_true',
        help='merge entire folder hierarchy')
    cmd.add_argument(
        'folders',
        nargs='*',
        help='list of folder ids to merge')

    cmd = sub.add_parser(
        'purge',
        help='purge folders (delete files and remove from database)')
    cmd.add_argument(
        'folders',
        nargs='*',
        help='list of folder ids to merge')
    
    
    args = parser.parse_args()
    
    if args.command:
        cli = CLI(args)
    else:
        parser.print_help()
