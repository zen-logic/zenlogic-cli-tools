import os, sys, pathlib, json
from core.filescan import FileScan
from core.filequery import FileQuery
from core.db_sqlite import Database


def home_dir():
    return pathlib.Path.home().resolve()

def script_dir():
    return pathlib.Path(__file__).parent.resolve()


class CLI(object):

    
    def __init__(self, db_file):
        db_file = os.path.join(script_dir(), db_file)
        db = Database(db_file)
     
        if not os.path.exists(db_file):
            db.run_sql_file('blank.sql')
            
        self.db = db


    def match(self, *args, **kwargs):
        # for key, value in kwargs.items():
        #     print("%s == %s" % (key, value))
        if 'file' in kwargs:
            query = FileQuery(self.db)
            for item in query.match_file(kwargs['file']):
                print(json.dumps(item))
        else:
            print('no file specified')

            
    def find(self, *args, **kwargs):
        query = FileQuery(self.db)
        if len(args) > 0:
            if args[0] == 'file':
                if len(args) > 1:
                    for item in query.find_file_name(args[1], case_insensitive=True):
                        print(json.dumps(item))
                else:
                    print('no file specified')
            elif args[0] == 'folder':
                if len(args) > 1:
                    for item in query.find_folder_name(args[1], case_insensitive=True):
                        print(json.dumps(item))
                else:
                    print('no folder specified')
            else:
                print('unrecognised type')
        else:
            print('specify "folder" or "file"')

    
    def roots(self, *args, **kwargs):
        query = FileQuery(self.db)
        print('Available storage roots:')
        for root in query.get_roots():
            print(str(root['id']).rjust(5), root['name'].ljust(20), root['path'])
    


if __name__ == '__main__':

    if len(sys.argv) > 1:
        command = sys.argv[1]
        args = []
        kwargs = {}
        for arg in sys.argv[2:]:
            if '=' in arg:
                key, value = arg.split('=')
                kwargs[key] = value
            else:
                args.append(arg)
        cli = CLI('test.db')
        if hasattr(cli, command):
            # run a method matching the command
            getattr(cli, command)(*args, **kwargs)
        else:
            print('%s command not found' % (command))
    else:
        print("usage: fh command [options]")
