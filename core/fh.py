import os, sys, pathlib, json
from filescan import FileScan
from filequery import FileQuery
from fileops import FileOps
from db_sqlite import Database


def home_dir():
    return pathlib.Path.home().resolve()

def script_dir():
    return pathlib.Path(__file__).parent.resolve()


class CLI(object):
    
    def __init__(self, db_file):
        db_file = os.path.join(script_dir(), db_file)
        self.fmt = 'json'
        self.fields = None
        self.db = Database(db_file)
        self.query = FileQuery(self.db)
        self.scan = FileScan(self.db)
        self.scan.verbose = True
        
        if not os.path.exists(db_file):
            blank = os.path.join(script_dir(), 'blank.sql')
            self.db.run_sql_file(blank)


    def output(self, data):
        if self.fmt == 'json':
            print(json.dumps(data))
        elif self.fmt == 'fields':
            out = []
            if self.fields == None:
                # show all fields
                fields = data.keys()
            else:
                # only selected fields
                fields = self.fields
                
            for field in fields:
                if field in data:
                    out.append(str(data[field]))
                else:
                    out.append(f'missing field: {field}')
            print(' | '.join(out))

            
    def match(self, *args, **kwargs):
        if 'file' in kwargs:
            for item in self.query.match_file(kwargs['file']):
                self.output(item)
        else:
            print('no file specified')

            
    def find(self, *args, **kwargs):
        if len(args) > 0:
            if args[0] == 'file':
                if len(args) > 1:
                    for item in self.query.find_file_name(args[1], case_insensitive=True):
                        self.output(item)
                else:
                    print('no file specified')
            elif args[0] == 'folder':
                if len(args) > 1:
                    for item in self.query.find_folder_name(args[1], case_insensitive=True):
                        self.output(item)
                else:
                    print('no folder specified')
            elif args[0] == 'hash':
                if len(args) > 1:
                    for item in self.query.find_hash(args[1]):
                        self.output(item)
                else:
                    print('no hash specified')
            elif args[0] == 'path':
                if len(args) > 1:
                    items = []
                    if len(args) > 2:
                        if args[1] == 'end':
                            items = self.query.find_path(args[2], end=True)
                        elif args[1] == 'start':
                            items = self.query.find_path(args[2], start=True)
                    else:
                        items = self.query.find_path(args[1])

                    for item in items:
                        self.output(item)
                else:
                    print('no path specified')
            else:
                print('unrecognised type')
        else:
            print('specify "folder" or "file"')

    
    def roots(self, *args, **kwargs):
        print('Available storage roots:')
        for root in self.query.get_roots():
            print(str(root['id']).rjust(5), root['name'].ljust(20), root['path'])


    def hierarchy(self, *args, **kwargs):
        if 'id' in kwargs:
            for folder in self.query.folder_hierarchy(kwargs['id']):
                # print(json.dumps(folder))
                print(folder['id'], folder['path'])
        else:
            print('specify folder id')


    def diff(self, *args, **kwargs):
        if 'src' in kwargs and 'dst' in kwargs:
            if 'all' in args:
                all = True
            else:
                all = False
            for folder in self.query.folder_diff(kwargs['src'], kwargs['dst'], all=all):
                self.output(folder)
        else:
            print('specify folder id for src and dst')


    def list(self, *args, **kwargs):
        if len(args) > 0:
            for item in self.query.list(args[0]):
                self.output(item)
        else:
            print('specify folder id for file list')
            
                

if __name__ == '__main__':
    opts = []; args = []; kwargs = {}
    if len(sys.argv) > 1:
        cli = CLI('test.db')
        command = sys.argv[1]
        for arg in sys.argv[2:]:
            if arg.startswith('-'):
                opts.append(arg)
            elif '=' in arg:
                key, value = arg.split('=')
                kwargs[key] = value
            else:
                args.append(arg)

        if 'fmt' in kwargs:
            cli.fmt = kwargs['fmt']

        if 'fields' in kwargs:
            cli.fields = kwargs['fields'].split(',')
            
        if hasattr(cli, command):
            getattr(cli, command)(*args, **kwargs)
        else:
            print('%s command not found' % (command))
    else:
        print("usage: fh command [options] [parameters]")
