import os, argparse
from cli_fm import CLI

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
        dest='command')
     
    # create the command parsers
    cmd = sub.add_parser(
        'get',
        help='get file by id')
    cmd.add_argument(
        'id',
        help='file id to retrieve')
    cmd.add_argument(
        'dst',
        help='where to copy the file')
    
    args = parser.parse_args()
    
    if args.command:
        cli = CLI(args)
    else:
        parser.print_help()
